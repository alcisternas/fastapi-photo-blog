# 📸 Photo Drop+  
**DevOps con FastAPI, Docker, Cloud Run, Jenkins, Google Cloud Storage y PostgreSQL**.  

---

## 🚀 Objetivo
- Subir una **foto**.  
- Agregar un **comentario**.  
- Guardar la foto en un **bucket GCS**.  
- Guardar el comentario + URL de la foto en una **base de datos PostgreSQL (Cloud SQL)**.  
- Consultar todas las fotos en `/photos`.  

Todo se desplegará en **Cloud Run** usando **Docker** y **Jenkins CI/CD**.  

---

## 📂 Estructura del proyecto
```
.
├── app/
│   ├── main.py        # FastAPI app
│   ├── gcs.py         # Manejo de Google Cloud Storage
│   ├── db.py          # Conexión a PostgreSQL
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
```

---

## 🛠️ Paso 1: Crear recursos en Google Cloud

1. **Activar servicios**:
   ```bash
   gcloud services enable run.googleapis.com sqladmin.googleapis.com artifactregistry.googleapis.com
   ```

2. **Crear un bucket en GCS**:
   ```bash
   BUCKET_NAME=photo-drop-bucket
   gsutil mb -l southamerica-west1 gs://$BUCKET_NAME
   ```

3. **Crear base de datos Cloud SQL (PostgreSQL)**:
   ```bash
   gcloud sql instances create photodb-instance        --database-version=POSTGRES_15        --tier=db-f1-micro        --region=southamerica-west1
   ```

4. **Crear base y usuario**:
   ```bash
   gcloud sql databases create photodb --instance=photodb-instance
   gcloud sql users create photouser --instance=photodb-instance --password=PhotoPass123
   ```

5. **Crear tabla**:
   ```sql
   CREATE TABLE photos (
     id SERIAL PRIMARY KEY,
     username VARCHAR(100),
     caption TEXT,
     url TEXT,
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

---

## 🐳 Paso 2: Empaquetar con Docker

```bash
docker build -t photoblog .
docker run -p 8000:8000 photoblog
```

Prueba en tu máquina:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)  

---

## ⚙️ Paso 3: Configurar Jenkins

1. Instalar Jenkins en una VM o contenedor.  
2. Crear un **pipeline** y pegar el contenido del `Jenkinsfile`.  
3. Configurar la credencial `gcp-sa-key` con un Service Account que tenga permisos en GCP.  

---

## 🤖 Jenkinsfile

El pipeline hace:
1. Checkout del código.  
2. Autenticación con GCP.  
3. Build + push de imagen a **Artifact Registry**.  
4. Despliegue en **Cloud Run**.  
5. Smoke test contra `/docs`.  

⚠️ Antes de correr el pipeline, exporta las variables necesarias:  
```groovy
--set-env-vars BUCKET_NAME=photo-drop-bucket,DB_CONN="postgresql://photouser:PhotoPass123@/photodb?host=/cloudsql/PROJECT:REGION:photodb-instance"
```

---

## 🌐 Paso 4: Desplegar en Cloud Run

Desde Jenkins (o local):
```bash
gcloud run deploy fastapi-demo   --image REGION-docker.pkg.dev/PROJECT/apps/fastapi-demo:latest   --platform managed   --region southamerica-west1   --allow-unauthenticated   --port 8000   --set-env-vars BUCKET_NAME=photo-drop-bucket,DB_CONN="postgresql://photouser:PhotoPass123@/photodb?host=/cloudsql/PROJECT:REGION:photodb-instance"
```

---

## 🎉 Paso 5: Probar la aplicación

1. Subir una foto:  
   - Endpoint: `POST /upload`  
   - Parámetros: `username`, `caption`, `file (imagen)`  
   - Devuelve: URL de la imagen.  

2. Ver todas las fotos:  
   - Endpoint: `GET /photos`  
   - Devuelve lista con `username`, `caption`, `url`.  

3. Revisar estado:  
   - Endpoint: `GET /healthz`  

---

## 🏆 Lo que aprenderán
- Cómo construir APIs con **FastAPI**.  
- Cómo contenerizar con **Docker**.  
- Cómo automatizar CI/CD con **Jenkins**.  
- Cómo desplegar en **Cloud Run**.  
- Cómo integrar servicios cloud (Storage + DB).  
