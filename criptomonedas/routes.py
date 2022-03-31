from criptomonedas import app
from flask import flash, render_template, request, redirect, url_for
import sqlite3
from criptomonedas.errors import APIError
from criptomonedas.models import CriptoValorModel, ProcesaDatos
from criptomonedas.forms import  PurchaseForm


ruta_db = app.config['RUTA_BBDD']
data_manager = ProcesaDatos(ruta_db)


@app.route("/")
def inicio():

    try:
        datos = data_manager.recupera_datos()
        
        return render_template("movimientos.html",movimientos = datos)
    except sqlite3.Error as e:
        flash("Se ha producido un error en la base de datos. Inténtelo de nuevo más tarde")
        return render_template("movimientos.html",movimientos = [])

@app.route("/purchase")
def compra():
    form = PurchaseForm()
   

    if request.method == 'GET':
        return render_template("compra.html", formulario = form)

    else:
        
        #validar datos
        if form.validate():
        #recuperar datos de form y calcular la tasa
            moneda_origen = str(form.moneda_from.data)
            moneda_destino = str(form.moneda_to.data)
            cantidad_origen = form.cantidad_from.data
            api_manager = CriptoValorModel(moneda_origen,moneda_destino)
            movimientos= []

            #Si hay valor en cantidad destino y se ha presionado el boton aceptar
            if form.cantidad_to.data and form.aceptar.data:
                cantidad_destino= form.cantidad_to.data
                #Introducir datos en base de datos
                data_manager.inserta_datos(params = [moneda_origen, cantidad_origen, moneda_destino, cantidad_destino])
                return redirect(url_for("inicio"))

            #Si no hay valor en cantidad destino y se ha presionado el boton calcular
            elif not form.cantidad_to and form.calcular.data:
               
                try:
                    tasa = api_manager.obtenerTasa()
                    cantidad_destino = cantidad_origen * tasa
                    #Crear formulario con la tasa consultada
                    
                    movimientos['cantidad_from']= cantidad_origen
                    movimientos['cantidad_to'] = cantidad_destino

                    form_datos = PurchaseForm(data = movimientos)

                    return render_template("compra.html",formulario =  form_datos, moneda_from = moneda_origen, moneda_to = moneda_destino)
                except APIError as e:
                    flash("Se ha producido un error al consultar la api")
                    return render_template("compra.html", formulario = form)
            
            #Si se da a cancelar, volver a inicio sin grabar datos
            elif form.cancelar.data:
                return redirect(url_for('inicio'))


        else:
            return render_template('compra.html',formulario = form)


@app.route("/status")
def estado():
    #consultar movimientos
    try:
        total_euros = data_manager.consuta_total_inversion()

        api_manager = CriptoValorModel()
        
        



        return render_template("status.html", contenido = "")

    except sqlite3.Error as e:
        flash("Se ha producido un error en la base de datos. Inténtelo de nuevo más tarde")
        return render_template("movimientos.html",movimientos = [])