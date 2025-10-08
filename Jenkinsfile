pipeline {
    agent any

    environment {
        VENV_PYTHON = "/opt/venv/bin/python3"
        PYTHON_SCRIPT = "scripts/analyze_log.py"
        OUTPUT_FILE = "${env.WORKSPACE}/ai_analysis_output.txt"
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {
        stage('Build') {
            steps {
                echo "\u001B[34m=== Starting Build Stage ===\u001B[0m"
                sh """
                    ${VENV_PYTHON} scripts/app.py
                """
            }
        }
    }

    post {
        failure {
            echo "\u001B[31m=== Build Failed: Running AI Log Analysis ===\u001B[0m"

            script {
                // Fetch full Jenkins console log
                def logText = currentBuild.rawBuild.getLog(999999).join("\n")

                // Write log to temporary file for Python
                def logFilePath = "${env.WORKSPACE}/jenkins_console_${env.BUILD_NUMBER}.txt"
                writeFile file: logFilePath, text: logText

                // Run AI analysis directly using venv Python
                sh """
                    ${VENV_PYTHON} ${PYTHON_SCRIPT} "${logFilePath}" "${OUTPUT_FILE}"
                """

                // Archive both console log and AI analysis
                archiveArtifacts artifacts: 'ai_analysis_output.txt, jenkins_console_*.txt', fingerprint: true
            }
        }

        always {
            echo "\u001B[32m=== Pipeline Finished ===\u001B[0m"
        }
    }
}
