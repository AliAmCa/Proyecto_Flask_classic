
class APIError(Exception):
    pass

def errorApi(e):
    if e.args[0]== 400:
        mensaje="Petición errónea"

    elif e.args[0]== 401:
        mensaje="API-KEY no válida"
    elif e.args[0]== 429:
        mensaje="Se ha excedido el máximo de peticiones con tu API-KEY "

    elif e.args[0]== 550:
        mensaje="No disponemos de datos de las monedas solicitadas"
    else:
        mensaje=""
    return mensaje