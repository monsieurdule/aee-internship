pipeline {
    agent {
        label 'vm' 
    }
        
    stages {
        stage('Test') { 
            steps {
                sh "python3 jenkinsadmin.py test"
            }
        }
    }
}