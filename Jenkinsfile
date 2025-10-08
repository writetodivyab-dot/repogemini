pipeline {
    agent { label 'master' }

    parameters {
        string(name: 'PR_NUMBER', defaultValue: '', description: 'PR number to post AI analysis to (leave empty for manual build only)')
    }

    environment {
		GEMINI_API_KEY = credentials('GEMINI_API_KEY')
        GITHUB_TOKEN   = credentials('GITHUB_TOKEN')
        REPO_FALLBACK  = "writetodivyab-dot/repogemini" // Remember to update this
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
                    // --- TEMPORARY DEBUGGING SCRIPT ---
                    // This will print the exact Python error to the console.
                    sh """
                        # The 'set +e' allows the script to continue so we can see all output.
                        set +e

                        echo "--- Attempting to install dependencies ---"
                        python3 -m pip install -r requirements.txt
                        # Check the exit code of the pip install command.
                        if [ \$? -ne 0 ]; then
                            echo "ERROR: 'pip install' failed. Check your requirements.txt file or Python setup."
                            exit 1
                        fi
                        echo "--- Dependencies installed successfully ---"

                        echo "--- Attempting to run app.py (output will appear below) ---"
                        python3 scripts/app.py
                        if [ \$? -ne 0 ]; then
                            echo "ERROR: Your app.py script failed to execute. The error message should be visible above this line."
                            exit 1
                        fi
                    """
                }
            }
        }
    }

    post {
        always {
            script {
                node('master') {
                    echo "\u001B[34m=== Post Build: Analyzing Logs ===\u001B[0m"

                    def logFile = "build_logs/build_${env.BUILD_NUMBER}.txt"
                    def prNumber = params.PR_NUMBER ?: null
                    def repoUrl = env.GIT_URL ?: "https://github.com/${env.REPO_FALLBACK}.git"

                    echo "Repository URL: ${repoUrl}"

                    def logExists = sh(script: "[ -f '${logFile}' ] && echo 'yes' || echo 'no'", returnStdout: true).trim()

                    if (logExists == 'yes') {
                        if (prNumber) {
                            echo "Posting AI analysis to PR #${prNumber}..."
                            sh """
                                GEMINI_API_KEY='${GEMINI_API_KEY}' \
                                GITHUB_TOKEN='${GITHUB_TOKEN}' \
                                python3 scripts/analyze_log.py '${logFile}' --pr ${prNumber} --repo ${repoUrl}
                            """
                        } else {
                            echo "Manual build (no PR), printing AI analysis to console..."
                            sh """
                                GEMINI_API_KEY='${GEMINI_API_KEY}' \
                                python3 scripts/analyze_log.py '${logFile}'
                            """
                        }
                    } else {
                        echo "\u001B[33mNo build log found at ${logFile}\u001B[0m"
                    }

                    archiveArtifacts artifacts: 'build_logs/*.txt', onlyIfSuccessful: false
                }
            }
        }
    }
}