# db.py (VERSIÓN COMPLETA Y CORREGIDA)
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
CLOUD_SQL_CONN = os.getenv("CLOUD_SQL_CONN")
DB_CONN_URL_LOCAL = os.getenv("DB_CONN") # para el fallback de DB_CONN

# --- LÓGICA DE CONEXIÓN ---

def get_db_connection():
    if CLOUD_SQL_CONN:
        return psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            host=f"/cloudsql/{CLOUD_SQL_CONN}", # Conexión Socket Unix
        )
    else:
        if DB_CONN_URL_LOCAL:
             return psycopg2.connect(DB_CONN_URL_LOCAL)
        else:
             raise Exception("Falta la configuración de la conexión a la base de datos (DB_USER/DB_PASS/DB_NAME o DB_CONN).")


# --- FUNCIONES DE DB (COMPLETADAS) ---

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