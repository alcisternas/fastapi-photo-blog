pipeline {
  agent any

  environment {
    REGION        = 'us-central1'
    REPO_NAME     = 'apps'
    SERVICE_NAME  = 'photo-drop'
    PROJECT_ID    = 'possible-sun-471215-d3'
    REGISTRY_HOST = "${REGION}-docker.pkg.dev"
    BUCKET_NAME   = 'photo-drop-bucket-ac'
    DB_USER       = 'photouser'
    DB_PASS       = 'yystww55s'
    DB_NAME       = 'photodb'
    // Se elimina CLOUD_SQL_CONN de aquí.
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
        sh """
          gcloud run deploy ${SERVICE_NAME} \\
            --image ${IMAGE} \\
            --platform managed \\
            --region ${REGION} \\
            --allow-unauthenticated \\
            --add-cloudsql-instances ${PROJECT_ID}:${REGION}:photodb-instance \\
            --set-env-vars BUCKET_NAME=${BUCKET_NAME},DB_USER=${DB_USER},DB_PASS=${DB_PASS},DB_NAME=${DB_NAME}
        """
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