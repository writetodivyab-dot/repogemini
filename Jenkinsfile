pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key')
        PYTHON_VENV = "/opt/venv/bin/python3"
        BUILD_LOG_DIR = "${WORKSPACE}/build_logs"
        REPO_FALLBACK = "writetodivyab-dot/repogemini"  // 🔹 CHANGE THIS
    }

    options {
        ansiColor('xterm')
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    sh "mkdir -p ${env.BUILD_LOG_DIR}"
                    try {
                        echo "\u001B[36mStarting build...\u001B[0m"
                        sh """
                            set -e
                            ${env.PYTHON_VENV} scripts/app.py > ${env.BUILD_LOG_DIR}/build_${env.BUILD_NUMBER}.txt 2>&1
                        """
                        echo "\u001B[32mBuild succeeded!\u001B[0m"
                    } catch (err) {
                        echo "\u001B[31mBuild failed, marking for analysis...\u001B[0m"
                        currentBuild.result = 'FAILURE'
                        throw err
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo "\u001B[34m=== Post Build: Analyzing Logs ===\u001B[0m"

                def logFile = "${env.BUILD_LOG_DIR}/build_${env.BUILD_NUMBER}.txt"
                def prNumber = env.CHANGE_ID ?: null
                def repoUrl = env.GIT_URL ?: "https://github.com/${env.REPO_FALLBACK}.git"

                echo "Repository URL: ${repoUrl}"

                if (fileExists(logFile)) {
                    if (prNumber) {
                        echo "Detected PR #${prNumber}, posting AI analysis comment..."
                        sh """
                            ${env.PYTHON_VENV} scripts/analyze_log.py ${logFile} --pr ${prNumber} --repo ${repoUrl}
                        """
                    } else {
                        echo "Manual build detected, writing AI analysis to console..."
                        sh """
                            ${env.PYTHON_VENV} scripts/analyze_log.py ${logFile}
                        """
                    }
                } else {
                    echo "\u001B[33mNo build log found at ${logFile}\u001B[0m"
                }
            }
            archiveArtifacts artifacts: 'build_logs/*.txt', onlyIfSuccessful: false
        }
    }
}
