pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mab3825/gap-prediction-app:latest'
        DOCKER_CREDENTIALS = 'docker-hub-credentials'  // Defined in Jenkins
        ADMIN_EMAIL = 'i211215@nu.edu.pk'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'master', url: 'https://github.com/M-Abdullah03/MLOPS_Assignment.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                docker context use default
                docker build -t %DOCKER_IMAGE% .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withDockerRegistry([credentialsId: DOCKER_CREDENTIALS, url: '']) {
                    bat 'docker push %DOCKER_IMAGE%'
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                bat '''
                docker stop gap-prediction-app || true
                docker rm gap-prediction-app || true
                docker pull %DOCKER_IMAGE%
                docker run -d --name gap-prediction-app -p 8000:8000 %DOCKER_IMAGE%
                '''
            }
        }

            stage('Send Notification') {
            steps {
              emailext(
                to: "${ADMIN_EMAIL}",
                subject: "Deployment Successful - Banking App",
                body: "The latest version has been deployed successfully!",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
               )
            }
        }
    }
}