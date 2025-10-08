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
        stage('Test Stage') {
            steps {
                sh 'echo "Step 2 Succeeded: Environment and credentials are OK."'
            }
        }
    }
}