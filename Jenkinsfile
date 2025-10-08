pipeline {
    agent any

    parameters {
        string(name: 'PR_NUMBER', defaultValue: '', description: 'PR number to post AI analysis to (leave empty for manual build only)')
    }

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key')
        GITHUB_TOKEN   = credentials('github-token')
        PYTHON_BIN     = "/opt/venv/bin/python3"  // Adjust if your Python path is different
        BUILD_LOG_DIR  = "${env.WORKSPACE}/build_logs"
        REPO_FALLBACK  = "writetodivyab-dot/repogemini"
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
                    sh "mkdir -p '${BUILD_LOG_DIR}'"
                    try {
                        echo "\u001B[36mStarting build...\u001B[0m"
                        sh """
                            set -e
                            ${PYTHON_BIN} scripts/app.py > '${BUILD_LOG_DIR}/build_${BUILD_NUMBER}.txt' 2>&1
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
            // Wrap in node to provide workspace context
            node('any') {
                script {
                    echo "\u001B[34m=== Post Build: Analyzing Logs ===\u001B[0m"

                    def logFile = "${BUILD_LOG_DIR}/build_${BUILD_NUMBER}.txt"
                    def prNumber = params.PR_NUMBER ?: null
                    def repoUrl = env.GIT_URL ?: "https://github.com/${REPO_FALLBACK}.git"

                    echo "Repository URL: ${repoUrl}"

                    // Check if log file exists
                    def logExists = sh(script: "[ -f '${logFile}' ] && echo 'yes' || echo 'no'", returnStdout: true).trim()

                    if (logExists == 'yes') {
                        if (prNumber) {
                            echo "Posting AI analysis to PR #${prNumber}..."
                            sh """
                                GEMINI_API_KEY='${GEMINI_API_KEY}' \
                                GITHUB_TOKEN='${GITHUB_TOKEN}' \
                                ${PYTHON_BIN} scripts/analyze_log.py '${logFile}' --pr ${prNumber} --repo ${repoUrl}
                            """
                        } else {
                            echo "Manual build (no PR), printing AI analysis to console..."
                            sh """
                                GEMINI_API_KEY='${GEMINI_API_KEY}' \
                                ${PYTHON_BIN} scripts/analyze_log.py '${logFile}'
                            """
                        }
                    } else {
                        echo "\u001B[33mNo build log found at ${logFile}\u001B[0m"
                    }

                    // Archive build logs
                    archiveArtifacts artifacts: 'build_logs/*.txt', onlyIfSuccessful: false
                }
            }
        }
    }
}
