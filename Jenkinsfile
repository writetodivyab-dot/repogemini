pipeline {
  agent any

  parameters {
    string(name: 'PR_NUMBER', defaultValue: '', description: 'Optional PR number to post to (for manual runs)')
  }

  environment {
    VENV_PYTHON = "/opt/venv/bin/python3"
    GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    GITHUB_TOKEN = credentials('GITHUB_TOKEN')

    // ✅ Hardcode your repo slug here (GitHub owner/repo)
    REPO_FALLBACK = 'writetodivyab-dot/repogemini'
  }

  stages {
    stage('Build') {
      steps {
        script {
          def consolePath = "${env.WORKSPACE}/build_logs/console_${env.BUILD_NUMBER}.txt"
          sh """
            #!/bin/bash
            set -o pipefail
            mkdir -p "${env.WORKSPACE}/build_logs"
            echo "Starting build; stdout/stderr will be saved to ${consolePath}"
            ${VENV_PYTHON} scripts/app.py 2>&1 | tee "${consolePath}"
          """
        }
      }
    }
  }

  post {
    failure {
      script {
        def logFile = "${env.WORKSPACE}/build_logs/console_${env.BUILD_NUMBER}.txt"

        def prNumber = env.CHANGE_ID ?: params.PR_NUMBER
        def repoName = env.REPO_FALLBACK
        if (!prNumber) { prNumber = "" }

        withEnv([
          "PR_NUMBER=${prNumber}",
          "REPO_NAME=${repoName}"
        ]) {
          sh """
            /opt/venv/bin/python3 scripts/analyze_log.py "${logFile}"
          """
        }
      }
      archiveArtifacts artifacts: 'build_logs/*.txt, ai_analysis_output.txt', fingerprint: true, allowEmptyArchive: true
    }

    always {
      archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true, allowEmptyArchive: true
    }
  }
}
