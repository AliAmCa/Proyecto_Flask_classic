import sqlite3
import requests
from config import API_KEY, URL_TASA_ESPECIFICA,MONEDAS, URL_ALL_RATES
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
        params2 =[fecha, hora]
        params2 = params2 + params
        self.consulta("""
        INSERT INTO movimientos (fecha, Hora, from, cantidad_from, to, cantidad_to)
                VALUES (?,?,?,?,?,?)
        """, params2)

    def consulta_total_inversion(self):
        
        datos = self.recupera_datos()
        totales =[]
        for moneda in MONEDAS:
            total_moneda=0.0
            cfrom=0.0
            cto=0.0
            
            for movimiento in datos:
                if movimiento['from'] == moneda:
                    cfrom += float(movimiento['cantidad_from'])
                if movimiento['to']== moneda:
                    cto+= float(movimiento['cantidad_to'])
            
            total_moneda=[]
            total_moneda.append(moneda)
            total_moneda.append(cto-cfrom)
            totales.append(total_moneda)
            
        return totales

    def consulta_euros_invertidos(self):
        datos = self.recupera_datos()
        total = 0.0
        for movimiento in datos:
            if movimiento['from'] == 'EUR':
                 total += float(movimiento['cantidad_from'])
        return total



class CriptoValorModel:
    
    def __init__(self, origen ="", destino = ""):
        self.apikey = API_KEY
        self.origen = origen
        self.destino= destino
        self.tasa = 0.0


    def obtenerTasa(self,origen, destino):
        self.origen = origen
        self.destino = destino

       
        respuesta = requests.get(URL_TASA_ESPECIFICA.format(self.origen, self.destino, self.apikey))
        
        if respuesta.status_code !=200:
            raise APIError(respuesta.status_code, respuesta.json()['error'])
        
        self.tasa = float(respuesta.json()['rate'])
        return self.tasa

    def conversorMoneda(self, cantidad):
        
        return cantidad * self.obtenerTasa()

    def obtener_cambio_a_euros(self):
        #Petición de todos los cambios de euros
        respuesta = requests.get(URL_ALL_RATES.format('EUR', self.apikey))

        if respuesta.status_code !=200:
            raise APIError(respuesta.status_code, respuesta.json()['error'])

        datos = respuesta.json()
        cambio_todos= []


        for dato in datos['rates']:
            if dato['asset_id_quote'] in MONEDAS:
                cambio =(dato['asset_id_quote'], (1/dato['rate']))
                cambio_todos.append(cambio)

        return cambio_todos
    
    
            




        



