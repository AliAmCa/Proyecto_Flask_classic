from criptomonedas import app
from flask import flash, render_template, request, redirect, url_for
import sqlite3


@app.route("/")
def inicio():

    return render_template("movimientos.html")