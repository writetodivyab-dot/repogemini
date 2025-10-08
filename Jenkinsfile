pipeline {
    agent any

    environment {
        LOG_DIR = "${env.WORKSPACE}/build_logs"
        PYTHON_SCRIPT = "scripts/analyze_log.py"
        OUTPUT_FILE = "${LOG_DIR}/ai_analysis_output.txt"
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
        VENV_PATH = "/var/jenkins_home/venv"
    }

    stages {
        stage('Build') {
            steps {
                echo "\u001B[34m=== Starting Build Stage ===\u001B[0m"
                sh """
                    mkdir -p '${LOG_DIR}'
                    source ${VENV_PATH}/bin/activate
                    echo "Running app.py..."
                    python3 scripts/app.py
                """
            }
        }
    }

    post {
        failure {
            echo "\u001B[31m=== Build Failed: Running AI Log Analysis ===\u001B[0m"

            script {
                // Save Jenkins console log to a file
                def logFilePath = "${LOG_DIR}/jenkins_console_${env.BUILD_NUMBER}.txt"
                def logText = currentBuild.rawBuild.getLog(999999).join("\n")
                writeFile file: logFilePath, text: logText

                // Run Python AI analysis
                sh """
                    source ${VENV_PATH}/bin/activate
                    python3 ${PYTHON_SCRIPT} \
                        "${logFilePath}" \
                        "${OUTPUT_FILE}"
                """
            }

            // Archive logs
            archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true, allowEmptyArchive: true
        }

        always {
            echo "\u001B[32m=== Pipeline Finished ===\u001B[0m"
        }
    }
}
