import sqlite3
import requests
from config import API_KEY, URL_TASA_ESPECIFICA,MONEDAS, URL_ALL_RATES, RUTA_BBDD
from criptomonedas.errors import APIError
from datetime import datetime


class ProcesaDatos:
    def __init__(self):
        self.origen_datos = RUTA_BBDD


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
        
        self.consulta("INSERT INTO movimientos (fecha,hora,moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?,?,?,?,?,?)", params)

    def consulta_total_inversion(self):
        
        datos = self.recupera_datos()
        totales =[]
        if datos:
            if isinstance(datos,dict):
                total_moneda=[]
                total_moneda.append(datos['moneda_to'])
                total_moneda.append(datos['cantidad_to'])

                totales.append(total_moneda)
            else:
                for moneda in MONEDAS:
                    total_moneda=0.0
                    cfrom=0.0
                    cto=0.0
                    
                    for movimiento in datos:
                        if movimiento['moneda_from'] == moneda:
                            cfrom += float(movimiento['cantidad_from'])
                        if movimiento['moneda_to']== moneda:
                            cto+= float(movimiento['cantidad_to'])
                    
                    if (cto-cfrom)>0:
                        total_moneda=[]
                        total_moneda.append(moneda)
                        total_moneda.append(cto-cfrom)

                        totales.append(total_moneda)
            
            
        return totales

    def consulta_euros_invertidos(self):
        datos = self.recupera_datos()
        totalInvertido = 0.0
        totalRecuperado = 0.0
        total= 0.0
        if isinstance(datos,dict):
            if datos['moneda_from'] == 'EUR':
                totalInvertido += float(datos['cantidad_from'])
            if datos['moneda_to'] == 'EUR':
                totalRecuperado += float(datos['cantidad_to'])
            total = totalInvertido -totalRecuperado
        else:
            for movimiento in datos:
                if movimiento['moneda_from'] == 'EUR':
                    totalInvertido += float(movimiento['cantidad_from'])
                if movimiento['moneda_to'] == 'EUR':
                    totalRecuperado += float(movimiento['cantidad_to'])
                total = totalInvertido -totalRecuperado
        return total
        
            

    def consulta_cantidad_moneda(self,moneda):
        datos = self.recupera_datos()
        total_from= 0.0
        total_to = 0.0
        if isinstance(datos,dict):
            if datos['moneda_from'] == moneda:
                total_from += float(datos['cantidad_from'])
            if datos['moneda_to'] == moneda:
                    total_to += float(datos['cantidad_to'])
        else:
            for movimiento in datos:
                if movimiento['moneda_from'] == moneda:
                    total_from += float(movimiento['cantidad_from'])
            
                if movimiento['moneda_to'] == moneda:
                    total_to += float(movimiento['cantidad_to'])

        return total_to - total_from


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
        cambio_todos= {}


        for dato in datos['rates']:
            if dato['asset_id_quote'] in MONEDAS:
                cambio_todos[dato['asset_id_quote']]= 1/dato['rate']

        return cambio_todos
    
    
            




        



