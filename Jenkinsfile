pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('gemini_api_key')
    }

    stages {
        stage('Setup') {
            steps {
                echo "Installing Python dependencies..."
                powershell '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                script {
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        def buildLog = "${env.WORKSPACE}\\build_logs\\build_output_${env.BUILD_NUMBER}.txt"
                        powershell """
                            mkdir -Force build_logs | Out-Null
                            python src/app.py *>&1 | Tee-Object -FilePath '${buildLog}'
                            if (\$LASTEXITCODE -ne 0) {
                                Write-Host "Build failed — captured logs to ${buildLog}" -ForegroundColor Red
                                exit 1
                            }
                        """
                    }
                }
            }
        }

        stage('Analyze Failure') {
            steps {
                script {
                    def buildLog = "${env.WORKSPACE}\\build_logs\\build_output_${env.BUILD_NUMBER}.txt"
                    def analysisFile = "${env.WORKSPACE}\\build_logs\\ai_analysis_${env.BUILD_NUMBER}.txt"

                    powershell """
                        Write-Host "Starting Gemini AI analysis..." -ForegroundColor Yellow
                        python scripts/analyze_log.py '${buildLog}' '${analysisFile}'
                        if (Test-Path '${analysisFile}') {
                            Write-Host "✅ Gemini AI analysis saved to ${analysisFile}" -ForegroundColor Green
                        } else {
                            Write-Host "⚠️  Gemini AI analysis file not created!" -ForegroundColor Red
                        }
                    """
                }
            }
        }

        stage('Archive Logs') {
            steps {
                script {
                    echo "Archiving build and analysis logs..."
                    archiveArtifacts artifacts: 'build_logs/*.txt', fingerprint: true
                }
            }
        }
    }

    post {
        always {
            script {
                def analysisFile = "${env.WORKSPACE}\\build_logs\\ai_analysis_${env.BUILD_NUMBER}.txt"
                def issuesDetected = false

                if (fileExists(analysisFile)) {
                    def lines = readFile(analysisFile).readLines()
                    issuesDetected = lines.find { it.startsWith("Known Issues:") } != null
                }

                if (currentBuild.currentResult == 'FAILURE') {
                    if (issuesDetected) {
                        echo "\033[91m🚨 Build failed with known issues detected! Check AI analysis artifacts.\033[0m"
                    } else {
                        echo "\033[93m⚠️  Build failed. No known issues detected, see AI analysis for details.\033[0m"
                    }
                    echo "\033[96m🔗 AI Analysis Artifact: build_logs/ai_analysis_${env.BUILD_NUMBER}.txt\033[0m"
                } else {
                    echo "\033[92m✅ Build succeeded! No errors detected.\033[0m"
                }
            }
        }
    }
}
