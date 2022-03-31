import sqlite3
import requests
from config import API_KEY, URL_TASA_ESPECIFICA
from criptomonedas.errors import APIError
from datetime import datetime


class ProcesaDatos:
    def __init__(self, file = ":memory:"):
        self.origen_datos = "data/movimientos.db"


    def crea_diccionario(self,cur):
        filas = cur.fetchall()
            
        campos = []
        for item in cur.description:
            campos.append(item[0])
        
        resultado =[]

        for fila in filas:

            #Creamos un diccionario
            registro = {}
            # Unimos en el diccionario los campos(clave) con su valor
            for clave,valor in zip(campos,fila):
                registro[clave] = valor
            resultado.append(registro)
        
        return resultado[0] if len(resultado)==1 else resultado

    
    def consulta(self, consulta, params= []):
        con= sqlite3.connect(self.origen_datos)
        cur = con.cursor()

        cur.execute(consulta, params)
        if cur.description: #si tiene contenido es un select, si esta vacio es una modificacion
            resultado = self.crea_diccionario(cur)

        else:
            resultado = None
            con.commit()
        con.close()
        return resultado

    def recupera_datos(self):
        return self.consulta("SELECT * FROM movimientos ORDER BY fecha")

    def inserta_datos(self, params):
        fecha = datetime.today().strftime('%d-%m-%Y')
        hora=datetime.today().strftime('%H:%M:%S')
        params2 =[]
        params2.append(fecha)
        params2.append(hora)
        params2 = params2 + params
        self.consulta("""
        INSERT INTO movimientos (fecha, hora, from, cantidad_from, to, cantidad_to)
                values (?,?,?,?,?,?)
        """, params2)

    def consuta_total_inversion(self):
        
        datos = self.recupera_datos()
        
        total_euros_invertidos = 0
        for movimiento in datos:
            if movimiento['from'] == 'EUR':
                total_euros_invertidos+= movimiento['cantidad_from']
        
        return total_euros_invertidos


class CriptoValorModel:
    def __init__(self, origen = "", destino = ""):
        self.apikey = API_KEY
        self.origen = origen
        self.destino= destino

        self.tasa = 0.0


    def obtenerTasa(self):
        
        time = datetime.today().strftime('%H:%M:%S')
        respuesta = requests.get(URL_TASA_ESPECIFICA.format(self.origen, self.destino,time, self.apikey))
        
        if respuesta.status_code !=200:
            raise APIError(respuesta.status_code, respuesta.json()['error'])
        
        self.tasa = round(respuesta.json()['rate'],2)
        return self.tasa

    def conversorMoneda(self):
        return self.origen * self.tasa