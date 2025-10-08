pipeline {
  agent any

  parameters {
    string(name: 'PR_NUMBER', defaultValue: '', description: 'Optional PR number for manual builds')
  }

  environment {
    VENV_PYTHON = "/opt/venv/bin/python3"
    GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    GITHUB_TOKEN = credentials('GITHUB_TOKEN')
    REPO_FALLBACK = 'writetodivyab-dot/repogemini'   // change this to your repo
  }

  stages {
    stage('Build') {
      steps {
        script {
          def logPath = "${env.WORKSPACE}/build_logs/console_${env.BUILD_NUMBER}.txt"
          sh """
            #!/bin/bash
            set -e
            mkdir -p "${env.WORKSPACE}/build_logs"
            echo "Simulating build, logs at ${logPath}"
            ${VENV_PYTHON} scripts/app.py 2>&1 | tee "${logPath}"
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

        withEnv([
          "PR_NUMBER=${prNumber}",
          "REPO_NAME=${repoName}"
        ]) {
          sh """
            #!/bin/bash
            set -e
            echo "Running AI analysis for failed build..."
            ${VENV_PYTHON} scripts/analyze_log.py "${logFile}"
          """
        }
      }
      archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true, allowEmptyArchive: true
    }

    always {
      archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true, allowEmptyArchive: true
    }
  }
}
