pipeline {
    agent any

    environment {
        APP_HOST = '127.0.0.1'
        APP_PORT = '5000'
        APP_URL  = "http://127.0.0.1:5000"
        VENV_DIR = "${WORKSPACE}/venv"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Start Flask Application') {
            steps {
                echo 'Starting Flask app in background on port 5000...'
                sh '''
                    nohup ${VENV_DIR}/bin/python app.py > flask.log 2>&1 &
                    echo $! > flask.pid
                    echo "Flask started with PID: $(cat flask.pid)"
                    sleep 5
                    echo "--- Flask startup log ---"
                    cat flask.log
                '''
            }
        }

        stage('Verify App is Running') {
            steps {
                echo 'Checking Flask is responding on port 5000...'
                sh '''
                    curl -s --retry 5 --retry-delay 2 \
                         --retry-connrefused \
                         http://127.0.0.1:5000 | head -5
                    echo "Flask is up and responding!"
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Running Selenium tests with pytest...'
                sh '${VENV_DIR}/bin/pytest tests/ -v --tb=short'
            }
        }

    }

    post {
        always {
            echo 'Stopping Flask application...'
            sh '''
                if [ -f flask.pid ]; then
                    kill $(cat flask.pid) || true
                    rm -f flask.pid flask.log
                fi
            '''
        }
        success {
            echo 'PIPELINE PASSED — All Selenium tests green!'
        }
        failure {
            echo 'PIPELINE FAILED — Check the stage logs above for details.'
        }
    }
}
