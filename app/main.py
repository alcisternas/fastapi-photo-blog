import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from app.gcs import upload_image_to_bucket
from app.db import save_metadata, list_photos

app = FastAPI(title="Photo Drop+", version="2.0.0")

BUCKET_NAME = os.getenv("BUCKET_NAME", "photo-drop-bucket")


@app.get("/")
def root():
    return {"message": "Bienvenido a Photo Drop+, sube tu foto con un comentario!"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/upload")
async def upload(
    username: str = Form(...),
    caption: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo imágenes por favor.")

    try:
        url = upload_image_to_bucket(file, BUCKET_NAME)
        save_metadata(username, caption, url)
        return {"message": "Foto subida con éxito!", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/photos")
def get_photos():
    return list_photos()
