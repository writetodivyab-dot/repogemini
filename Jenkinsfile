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
                    sh 'python3 -m pip install -r requirements.txt'
                    sh "mkdir -p build_logs"
                    try {
                        echo "\u001B[36mStarting build...\u001B[0m"
                        sh """
                            # Run the python script and redirect all output to the log file.
                            python3 scripts/app.py > 'build_logs/build_${BUILD_NUMBER}.txt' 2>&1

                            # Save the exit code of the python script. 0 is success, anything else is failure.
                            STATUS=\$?

                            # Exit with the same status code. If it's non-zero, the 'catch' block will run.
                            exit \$STATUS
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
