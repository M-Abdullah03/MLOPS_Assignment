pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mab3825/banking-app:latest'
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
                bat 'docker build -t $env.DOCKER_IMAGE .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withDockerRegistry([credentialsId: DOCKER_CREDENTIALS, url: '']) {
                    bat 'docker push $env.DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                bat '''
                docker stop banking-app || true
                docker rm banking-app || true
                docker pull $env.DOCKER_IMAGE
                docker run -d --name banking-app -p 8000:8000 $env.DOCKER_IMAGE
                '''
            }
        }

        stage('Send Notification') {
            steps {
                mail to: "$env.ADMIN_EMAIL",
                     subject: "Deployment Successful - Banking App",
                     body: "The latest version has been deployed successfully!"
            }
        }
    }
}