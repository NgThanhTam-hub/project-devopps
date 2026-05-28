pipeline {
    agent any

    environment {
        APP_NAME  = "k8s-cicd-app"
        IMAGE_TAG = "build-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "===== Stage 1: Checkout ====="
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                echo "===== Stage 2: Unit Tests ====="
                sh '''
                    pip3 install -r app/requirements.txt \
                        --break-system-packages --quiet
                    python3 -m pytest app/test_app.py -v \
                        --tb=short
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "===== Stage 3: Build Image ====="
                sh """
                    docker build -t ${APP_NAME}:${IMAGE_TAG} .
                    docker tag  ${APP_NAME}:${IMAGE_TAG} \
                                ${APP_NAME}:latest
                """
            }
        }

        stage('Deploy') {
            steps {
                echo "===== Stage 4: Deploy ====="
                sh """
                    docker stop ${APP_NAME} || true
                    docker rm   ${APP_NAME} || true
                    docker run -d \
                        --name ${APP_NAME} \
                        -p 5000:5000 \
                        --restart unless-stopped \
                        ${APP_NAME}:latest
                """
            }
        }

        stage('Health Check') {
            steps {
                echo "===== Stage 5: Health Check ====="
                sh '''
                    sleep 3
                    curl -sf http://localhost:5000/health || exit 1
                    echo "App is healthy!"
                '''
            }
        }
    }

    post {
        success {
            echo "================================="
            echo " SUCCESS - Build #${BUILD_NUMBER}"
            echo " http://192.168.171.100:5000"
            echo "================================="
        }
        failure {
            echo "================================="
            echo " FAILED - Build #${BUILD_NUMBER}"
            echo "================================="
            sh "docker stop ${APP_NAME} || true"
            sh "docker rm   ${APP_NAME} || true"
        }
    }
}
