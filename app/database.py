import os
import mysql.connector
from flask import g # Importa g de flask para almacenar datos durante la petición
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Confifuración de la base de datos usando variables de entorno

DATABASE_CONFIG = {
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 3306),
}

# Función para obtener la conexión de la base de datos
def get_db():
    # Si no hay una conexión a la base de datos en g, la creamos
    # g, que es un objeto de flask que se usa para almacenar datos durante la vida util de una petición
    if 'db' not in g:
        print("...Abriendo conexión con la base de datos...")
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    # Retorna la conexión a la base de datos
    return g.db


# Función para cerrar la conexión con la base de datos
def close_db(e=None):
    # Intenta obtener la conexión a la base de datos desde g
    db = g.pop('db', None)
    # Si hay una conexión, la cerramos
    if db is not None:

        print("..Cerrando conexión con la base de datos...")
        db.close()

# Función para inicializar la aplición con el cierre automático de la base de datos
def init_app(app):
    # Registrar la funci+on close_db para que se llame automáticamente
    # cuando el contexto de la aplicación se destruye
    app.teardown_appcontext(close_db)
