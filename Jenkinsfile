pipeline {
    agent any

    environment {
        LOG_DIR = "${env.WORKSPACE}/build_logs"
        PYTHON_SCRIPT = "scripts/analyze_log.py"
        OUTPUT_FILE = "${env.LOG_DIR}/ai_analysis_output.txt"
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {
        stage('Build') {
            steps {
                echo "\u001B[34m=== Starting Build Stage ===\u001B[0m"
                // Use Linux shell commands instead of bat
                sh '''
                    echo "Building project..."
					python3 scripts/app.py
                    echo "Running tests..."
                    echo "All steps executed successfully!"
                '''
            }
        }

        stage('Analyze Failure') {
            when {
                expression { currentBuild.resultIsWorseOrEqualTo('FAILURE') }
            }
            steps {
                script {
                    echo "\u001B[33m=== Extracting Jenkins Build Log ===\u001B[0m"

                    sh "mkdir -p '${LOG_DIR}'"

                    def logFilePath = "${LOG_DIR}/jenkins_console_${env.BUILD_NUMBER}.txt"
                    def logText = currentBuild.rawBuild.getLog(999999).join("\n")
                    writeFile file: logFilePath, text: logText

                    echo "\u001B[36m=== Running AI Log Analysis (Gemini) ===\u001B[0m"
                    sh """
                        python3 "${PYTHON_SCRIPT}" \
                            "${logFilePath}" \
                            "${OUTPUT_FILE}"
                    """
                }
            }
        }

        stage('Archive Logs') {
            steps {
                echo "\u001B[35m=== Archiving Logs and Analysis Output ===\u001B[0m"
                archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "\u001B[32m=== Build succeeded! ===\u001B[0m"
        }
        failure {
            echo "\u001B[31m=== Build failed! Running analysis anyway... ===\u001B[0m"
        }
    }
}
