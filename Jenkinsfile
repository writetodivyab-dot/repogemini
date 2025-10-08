pipeline {
    agent any

    // Manual PR parameter
    parameters {
        string(name: 'PR_NUMBER', defaultValue: '', description: 'PR number to post AI analysis to (leave empty for manual build only)')
    }

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key')   // Jenkins credential
        GITHUB_TOKEN   = credentials('github-token')    // Jenkins GitHub token
        PYTHON_VENV    = "/opt/venv/bin/python3"        // Path to Python in your Jenkins container
        BUILD_LOG_DIR  = "${env.WORKSPACE}/build_logs"
        REPO_FALLBACK  = "writetodivyab-dot/repogemini"  // Replace with your repo
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
                    // Ensure log folder exists
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
            // Wrap in node to get workspace context
            node {
                script {
                    echo "\u001B[34m=== Post Build: Analyzing Logs ===\u001B[0m"

                    def logFile = "${BUILD_LOG_DIR}/build_${BUILD_NUMBER}.txt"
                    def prNumber = params.PR_NUMBER ?: null
                    def repoUrl = env.GIT_URL ?: "https://github.com/${REPO_FALLBACK}.git"

                    echo "Repository URL: ${repoUrl}"

                    // Check if build log exists
                    def logExists = sh(script: "[ -f '${logFile}' ] && echo 'yes' || echo 'no'", returnStdout: true).trim()

                    if (logExists == 'yes') {
                        if (prNumber) {
                            echo "Posting AI analysis to PR #${prNumber}..."
                            sh """
                                GEMINI_API_KEY='${GEMINI_API_KEY}' \
                                GITHUB_TOKEN='${GITHUB_TOKEN}' \
                                ${PYTHON_VENV} scripts/analyze_log.py '${logFile}' --pr ${prNumber} --repo ${repoUrl}
                            """
                        } else {
                            echo "Manual build (no PR), printing AI analysis to console..."
                            sh """
                                GEMINI_API_KEY='${GEMINI_API_KEY}' \
                                ${PYTHON_VENV} scripts/analyze_log.py '${logFile}'
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
