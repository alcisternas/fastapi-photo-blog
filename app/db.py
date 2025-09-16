import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONN = os.getenv("DB_CONN")  # ej: postgresql://user:pass@host:5432/photodb


def save_metadata(username, caption, url):
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO photos (username, caption, url) VALUES (%s, %s, %s)",
        (username, caption, url),
    )
    conn.commit()
    cur.close()
    conn.close()


def list_photos():
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT username, caption, url FROM photos ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
