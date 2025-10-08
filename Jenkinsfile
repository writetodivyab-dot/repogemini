pipeline {
    agent { label 'master' }

    parameters {
        string(name: 'PR_NUMBER', defaultValue: '', description: 'PR number to post AI analysis to (leave empty for manual build only)')
    }

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
        GITHUB_TOKEN   = credentials('GITHUB_TOKEN')
        REPO_FALLBACK  = "writetodivyab-dot/repogemini"
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
                    sh "mkdir -p build_logs"
                    try {
                        echo "\u001B[36mStarting build...\u001B[0m"
                        sh """
                            set -e
                            python3 scripts/app.py > 'build_logs/build_${BUILD_NUMBER}.txt' 2>&1
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
}