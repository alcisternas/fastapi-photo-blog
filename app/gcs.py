import uuid
from google.cloud import storage


def upload_image_to_bucket(file, bucket_name: str) -> str:
    """
    Sube la imagen a GCS y retorna la URL pública.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Nombre único para evitar colisiones
    blob_name = f"{uuid.uuid4()}-{file.filename}"
    blob = bucket.blob(blob_name)

    # Subir archivo en memoria
    blob.upload_from_file(file.file, content_type=file.content_type)

    # Hacerlo público
    blob.make_public()

    return blob.public_url
