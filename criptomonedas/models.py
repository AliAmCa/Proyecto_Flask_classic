import sqlite3

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