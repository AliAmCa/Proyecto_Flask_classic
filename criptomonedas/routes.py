from criptomonedas import app
from flask import flash, render_template, request, redirect, url_for
import sqlite3
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
def purchase():
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
            try:
                tasa = api_manager.obtenerTasa()
                cantidad_destino = cantidad_origen * tasa
                #Crear formulario con la tasa consultada
                movimientos['moneda_from']= moneda_origen
                movimientos['moneda_to']= moneda_destino
                movimientos['cantidad_from']= cantidad_origen

                form_datos = PurchaseForm(data = movimientos)

                return render_template("compra.html",formulario =  form_datos, total = cantidad_destino)
            except:
                flash("Se ha producido un error al consultar la api")
                return render_template("compra.html", formulario = form)



            #Si se da a aceptar, pasar los datos al modelo para que los grabe


        else:
            return render_template('compra.html',formulario = form)