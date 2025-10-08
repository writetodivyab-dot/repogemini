pipeline {
    agent any

    environment {
        VENV_PATH = "/opt/venv"
        PYTHON_SCRIPT = "scripts/analyze_log.py"
        OUTPUT_FILE = "${env.WORKSPACE}/ai_analysis_output.txt"
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {
        stage('Build') {
            steps {
                echo "\u001B[34m=== Starting Build Stage ===\u001B[0m"
                sh """
                    source ${VENV_PATH}/bin/activate
                    python3 scripts/app.py
                """
            }
        }
    }

    post {
        failure {
            echo "\u001B[31m=== Build Failed: Running AI Log Analysis ===\u001B[0m"

            script {
                // Fetch console log directly
                def logText = currentBuild.rawBuild.getLog(999999).join("\n")

                // Write to temporary file for analyze_log.py
                def logFilePath = "${env.WORKSPACE}/jenkins_console_${env.BUILD_NUMBER}.txt"
                writeFile file: logFilePath, text: logText

                // Run Gemini AI analysis
                sh """
                    source ${VENV_PATH}/bin/activate
                    python3 ${PYTHON_SCRIPT} "${logFilePath}" "${OUTPUT_FILE}"
                """

                // Archive AI analysis and console log
                archiveArtifacts artifacts: 'ai_analysis_output.txt, jenkins_console_*.txt', fingerprint: true
            }
        }

        always {
            echo "\u001B[32m=== Pipeline Finished ===\u001B[0m"
        }
    }
}
