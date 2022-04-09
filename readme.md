# myCriptos

Aplicación de control de valores en criptomonedas

## Creación BBDD

El fichero `crea_tabla.sql` contiene el modelo a seguir para crear la base de datos.

## Fichero .env

Debes hacer lo siguiente:

1. Copiar el fichero `.env_template` y elegir una de las opciones de `FLASK_ENV`:

    ```
    FLASK_ENV = <tu opción aquí>
    ```
2. Renombrar el fichero como `.env`


## SECRET_KEY
Debes generar una secret-key, por ejemplo con randomkeygen.com

## API_KEY
Debes pedir una API KEY a la página coinAPI.io

## Fichero .config
Copiar el fichero `config_template`:
    ```
    cp config_template.py config.py
    ```

Después debes hacer lo siguiente:
1. Introducir la ruta a tu BBDD en el nuevo fichero
    ```
    RUTA_BBDD = <tu ruta aquí>
    ```
2. Introducir tu SECRET KEY en el nuevo fichero
    ```
    SECRET_KEY = <tu clave aquí>
    ```
3. Introducir tu API KEY en el nuevo fichero
    ```
    API_KEY = <tu clave aquí>
    ```
4. Renombrar el fichero como `config.py`

