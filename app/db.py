# db.py (Código modificado - MÍNIMO)
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Variables del entorno (ahora definidas por el Jenkinsfile)
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
# La variable de conexión al socket que Cloud Run configura
CLOUD_SQL_CONN = os.getenv("CLOUD_SQL_CONN")

# Función de conexión modificada
def get_db_connection():
    # Construye el path del socket. El host es el path del directorio que contiene el socket.
    # El nombre de la instancia DEBE ser el host del socket
    # Si Cloud Run está desplegado con --add-cloudsql-instances, usará el socket.
    # Nota: Si DB_CONN viene de Jenkins, se usa ese valor.
    
    # Intenta usar la conexión de Cloud Run (usando el nombre de conexión como Host)
    if CLOUD_SQL_CONN:
        return psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            host=f"/cloudsql/{CLOUD_SQL_CONN}", # Directorio que contiene el socket
        )
    else:
        # Fallback para desarrollo local (si usaras DB_CONN URL)
        db_conn_url = os.getenv("DB_CONN")
        if db_conn_url:
             return psycopg2.connect(db_conn_url)
        else:
             raise Exception("Falta la configuración de la conexión a la base de datos.")


# Modificar las funciones save_metadata y list_photos para usar get_db_connection()

def save_metadata(username, caption, url):
    conn = get_db_connection()
    # ...
    
def list_photos():
    conn = get_db_connection()
    # ...
    return rows
