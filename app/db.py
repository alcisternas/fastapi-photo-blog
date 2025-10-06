import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
# Esta variable es inyectada automáticamente por Cloud Run al usar --add-cloudsql-instances
CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")
# Esta es para el fallback/desarrollo local.
DB_CONN_URL_LOCAL = os.getenv("DB_CONN")

# --- LÓGICA DE CONEXIÓN ---

def get_db_connection():
    # 1. Conexión a Cloud SQL con Socket Unix
    if CLOUD_SQL_CONNECTION_NAME:
        return psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            # La ruta del host es el directorio del socket
            host=f"/cloudsql/{CLOUD_SQL_CONNECTION_NAME}", 
        )
    # 2. Conexión de fallback (para desarrollo local)
    elif DB_CONN_URL_LOCAL:
         return psycopg2.connect(DB_CONN_URL_LOCAL)
    else:
         # Si la aplicación falla aquí al inicio, es porque faltan las variables en el contenedor
         raise Exception("Falta la configuración de la conexión a la base de datos (DB_USER/DB_PASS/DB_NAME o DB_CONN).")


# --- FUNCIONES DE DB ---

def save_metadata(username, caption, url):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO photos (username, caption, url) VALUES (%s, %s, %s)",
            (username, caption, url),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def list_photos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT username, caption, url FROM photos ORDER BY id DESC")
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()