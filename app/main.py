import os
import uuid
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from google.cloud import storage
import psycopg2

app = FastAPI(title="PhotoBlog", version="1.0.0")

# Variables de entorno
BUCKET_NAME = os.getenv("BUCKET_NAME")
DB_CONN = os.getenv("DB_CONN")  # ej: "postgresql://user:pass@host:5432/dbname"

# Cliente global GCS
gcs_client = storage.Client()

def save_to_db(username, caption, url):
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO photos (username, caption, url, created_at) VALUES (%s, %s, %s, %s)",
        (username, caption, url, datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()

@app.post("/upload")
async def upload_photo(
    username: str = Form(...),
    caption: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo imágenes por favor.")

    # Subir imagen a GCS
    blob_name = f"{uuid.uuid4()}-{file.filename}"
    bucket = gcs_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()
    url = blob.public_url

    # Guardar metadata en la DB
    save_to_db(username, caption, url)

    return {"message": "Foto subida con éxito", "url": url}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
