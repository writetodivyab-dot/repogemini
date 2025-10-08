pipeline {
    agent any

    parameters {
        string(name: 'PR_NUMBER', defaultValue: '', description: 'PR number to post AI analysis to (leave empty for manual build only)')
    }

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key')
        PYTHON_VENV = "/opt/venv/bin/python3"
        BUILD_LOG_DIR = "${WORKSPACE}/build_logs"
        REPO_FALLBACK = "writetodivyab-dot/repogemini"
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
                            ${PYTHON_VENV} scripts/app.py > '${BUILD_LOG_DIR}/build_${BUILD_NUMBER}.txt' 2>&1
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

                // Use dir() to ensure workspace context
                dir("${WORKSPACE}") {
                    def logFile = "${BUILD_LOG_DIR}/build_${BUILD_NUMBER}.txt"
                    def prNumber = params.PR_NUMBER ?: null
                    def repoUrl = env.GIT_URL ?: "https://github.com/${REPO_FALLBACK}.git"

                    echo "Repository URL: ${repoUrl}"

                    // Check log file existence using sh/readFile instead of fileExists
                    def logExists = sh(script: "[ -f '${logFile}' ] && echo 'yes' || echo 'no'", returnStdout: true).trim()

                    if (logExists == 'yes') {
                        if (prNumber) {
                            echo "Posting AI analysis to PR #${prNumber}..."
                            sh """
                                ${PYTHON_VENV} scripts/analyze_log.py '${logFile}' --pr ${prNumber} --repo ${repoUrl}
                            """
                        } else {
                            echo "Manual build (no PR), printing AI analysis to console..."
                            sh """
                                ${PYTHON_VENV} scripts/analyze_log.py '${logFile}'
                            """
                        }
                    } else {
                        echo "\u001B[33mNo build log found at ${logFile}\u001B[0m"
                    }

                    // Archive artifacts (works in dir context)
                    archiveArtifacts artifacts: 'build_logs/*.txt', onlyIfSuccessful: false
                }
            }
        }
    }
}
