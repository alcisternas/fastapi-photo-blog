pipeline {
  agent any

  environment {
    REGION        = 'southamerica-west1'
    REPO_NAME     = 'apps'
    SERVICE_NAME  = 'photo-drop'
    PROJECT_ID    = 'durable-ring-471120-i8'
    REGISTRY_HOST = "${REGION}-docker.pkg.dev"
    BUCKET_NAME   = 'photo-drop-bucket'
    DB_CONN       = 'postgresql://photouser:PhotoPass123@/photodb?host=/cloudsql/durable-ring-471120-i8:southamerica-west1:photodb-instance'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Auth GCP') {
      steps {
        withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
            gcloud config set project ${PROJECT_ID}
            gcloud auth configure-docker ${REGISTRY_HOST} -q
          '''
        }
      }
    }

    stage('Build & Push Image') {
      steps {
        script {
          def COMMIT = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
          env.IMAGE = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:${COMMIT}"
        }
        sh '''
          docker build -t "${IMAGE}" .
          docker push "${IMAGE}"
        '''
      }
    }

    stage('Deploy Cloud Run') {
      steps {
        sh '''
          gcloud run deploy ${SERVICE_NAME} \
            --image ${IMAGE} \
            --platform managed \
            --region ${REGION} \
            --allow-unauthenticated \
            --set-env-vars BUCKET_NAME=${BUCKET_NAME},DB_CONN=${DB_CONN}
        '''
      }
    }
  }

  post {
    success {
      echo "✅ Despliegue OK"
    }
    failure {
      echo "❌ Error en el pipeline"
    }
  }
}
