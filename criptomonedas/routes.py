from criptomonedas import app
from flask import flash, render_template, request, redirect, url_for
import sqlite3
from criptomonedas.models import ProcesaDatos
from criptomonedas.forms import PurchaseForm
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