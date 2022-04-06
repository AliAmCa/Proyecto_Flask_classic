from criptomonedas import app
from flask import flash, render_template, request, redirect, url_for
import sqlite3
from criptomonedas.errors import APIError
from criptomonedas.models import CriptoValorModel, ProcesaDatos
from criptomonedas.forms import  PurchaseForm
from datetime import datetime


#ruta_db = app.config['RUTA_BBDD']
data_manager = ProcesaDatos()
api_manager = CriptoValorModel()

@app.route("/")
def inicio():

    try:
        datos = data_manager.recupera_datos()
        
        return render_template("movimientos.html",movimientos = datos)
    except sqlite3.Error as e:
        flash("Se ha producido un error en la base de datos. Inténtelo de nuevo más tarde")
        return render_template("movimientos.html",movimientos = [])

@app.route("/purchase", methods= ['GET', 'POST'])
def purchase():
    form = PurchaseForm()
   
    choices = ['EUR','ETH','BNB','LUNA','SOL','BTC','BCH','LINK','ATOM','USDT']
    if request.method == 'GET':
        return render_template("compra.html", formulario = form)

    else:
        
        #validar datos
        if form.validate():
        #recuperar datos de form y calcular la tasa
            moneda_origen = choices[int(form.moneda_from.data)]
            moneda_destino = choices[int(form.moneda_to.data)]
            cantidad_origen = form.cantidad_from.data
           
            #Si se da a cancelar, volver a inicio sin grabar datos
            
            if form.cancelar.data:
                return redirect(url_for('inicio'))


            if moneda_destino == moneda_origen:
                flash("La moneda destino no puede ser igual a la moneda origen")
                return render_template("compra.html", formulario = form)


            #Si se ha presionado el boton aceptar
            if  form.aceptar.data:
                try:
                    tasa = api_manager.obtenerTasa(moneda_origen,moneda_destino)
                    cantidad_destino = cantidad_origen * tasa
                    fecha = datetime.today().strftime('%d-%m-%Y')
                    hora=datetime.today().strftime('%H:%M:%S')
                    #Introducir datos en base de datos
                    data_manager.inserta_datos(params = (fecha, hora,moneda_origen, cantidad_origen, moneda_destino, cantidad_destino))
                    return redirect(url_for("inicio"))
                except sqlite3.Error as e:
                    flash("Se ha producido un error en la base de datos. Inténtelo de nuevo más tarde")
                    return render_template("compra.html", formulario = form)

            #Si no hay valor en cantidad destino y se ha presionado el boton calcular
            elif form.calcular.data:
                
                try:
                    tasa = api_manager.obtenerTasa(moneda_origen,moneda_destino)
                    cantidad_destino = cantidad_origen * tasa
                    #Crear formulario con la tasa consultada
                   
                    return render_template("compra.html",formulario =  form, cantidad_to = cantidad_destino  )
                except APIError as e:
                    flash("Se ha producido un error al consultar la api")
                    return render_template("compra.html", formulario = form)
            

        else:
            flash("Datos no válidos")
            return render_template('compra.html',formulario = form)


@app.route("/status")
def estado():
    
    #consultar movimientos
    try:
        totales = data_manager.consulta_total_inversion()
        cambios = api_manager.obtener_cambio_a_euros()
        resultados =[]
        
        valor = 0.0
        invertido = data_manager.consulta_euros_invertidos()
        for total_moneda in totales:
            moneda =total_moneda[0]
            cantidad_moneda = total_moneda[1]
            total_eur=0
            for moneda_c in cambios:
                if moneda == moneda_c[0]:
                    total_eur= cantidad_moneda * moneda_c[1]
                valor += total_eur
            else:
                valor += cantidad_moneda

        resultados.append(invertido)
        resultados.append(valor)

        return render_template("status.html", contenido = resultados, invertido = resultados[0], valor = round(resultados[1],2))

    except sqlite3.Error as e:
        flash("Se ha producido un error en la base de datos. Inténtelo de nuevo más tarde")
        return render_template("movimientos.html",movimientos = [])