pipeline {
    agent any

    environment {
        // Python
        VENV_NAME = "venv"
        APP_PORT = "8005"
        PYTHONPATH = "${WORKSPACE}"

        // MLflow
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "llm-customer-support"

        // Docker Images
        IMAGE_CPU = "llm-customer-support:cpu"
        IMAGE_GPU = "llm-customer-support:gpu"
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
        timestamps()
    }

    stages {

        /* ================================
           1. Checkout
        ================================= */
        stage("Checkout Code") {
            steps {
                git branch: "master",
                    url: "https://github.com/anjilinux/project-mlflow-LLM-Use-Cases-In-Customer-Experience-And-Support.git"
            }
        }

        /* ================================
           2. Load .env
        ================================= */
        stage("Load Environment Variables") {
            steps {
                sh '''
                if [ -f .env ]; then
                    export $(grep -v '^#' .env | xargs)
                    echo "✅ .env loaded"
                else
                    echo "⚠️ .env not found"
                fi
                '''
            }
        }

        /* ================================
           3. Setup Python VirtualEnv
        ================================= */
        stage("Setup Virtual Environment") {
            steps {
                sh '''
                python3 -m venv $VENV_NAME
                . $VENV_NAME/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        /* ================================
           4. Validate Knowledge Base
        ================================= */
        stage("Validate sample_faqs.txt") {
            steps {
                sh '''
                test -f sample_faqs.txt
                echo "✅ sample_faqs.txt found"
                '''
            }
        }

        /* ================================
           5. Lint
        ================================= */
        stage("Lint") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python -m py_compile \
                    app.py llm_client.py rag.py vector_store.py \
                    prompts.py config.py monitor.py logger.py \
                    ingest_data.py schema.py
                '''
            }
        }

        /* ================================
           6. Unit Tests
        ================================= */
        stage("Pytests") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                pytest -v
                '''
            }
        }

        /* ================================
           7. Schema Validation
        ================================= */
        stage("Schema Validation") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python schema.py
                '''
            }
        }

        /* ================================
           8. Vector Store
        ================================= */
        stage("Vector Store") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python - <<EOF
import vector_store
print("✅ vector_store loaded")
EOF
                '''
            }
        }

        /* ================================
           9. Prompts
        ================================= */
        stage("Prompts") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python - <<EOF
import prompts
print("✅ prompts loaded")
EOF
                '''
            }
        }

        /* ================================
           10. Monitor
        ================================= */
        stage("Monitor") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python - <<EOF
import monitor
print("✅ monitor loaded")
EOF
                '''
            }
        }

        /* ================================
           11. Logger
        ================================= */
        stage("Logger") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python - <<EOF
import logger
print("✅ logger loaded")
EOF
                '''
            }
        }

        /* ================================
           12. Config + MLflow
        ================================= */
        stage("Config & MLflow") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
                python - <<EOF
import config
print("✅ config + MLflow loaded")
EOF
                '''
            }
        }

        /* ================================
           13. LLM Client
        ================================= */
        stage("LLM Client") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python - <<EOF
import llm_client
print("✅ llm_client loaded")
EOF
                '''
            }
        }

        /* ================================
           14. Ingest Data
        ================================= */
        stage("Ingest Data") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python ingest_data.py
                '''
            }
        }

        /* ================================
           15. RAG Pipeline
        ================================= */
        stage("RAG Pipeline") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python rag.py
                '''
            }
        }

        /* ================================
           16. FastAPI Import
        ================================= */
        stage("FastAPI Import") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python - <<EOF
from app import app
print("✅ FastAPI app import OK")
EOF
                '''
            }
        }

        /* ================================
           17. FastAPI Smoke Test (Local)
        ================================= */
        stage("FastAPI Smoke Test") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                nohup uvicorn app:app \
                  --host 0.0.0.0 \
                  --port $APP_PORT > uvicorn.log 2>&1 &

                sleep 5
                curl -f http://localhost:$APP_PORT/health
                pkill -f "uvicorn app:app" || true
                '''
            }
        }

        /* ================================
           18. Docker Build (CPU)
        ================================= */
        stage("Docker Build CPU") {
            steps {
                sh '''
                docker build -t $IMAGE_CPU .
                '''
            }
        }

        /* ================================
           19. Docker Build (GPU)
        ================================= */
        stage("Docker Build GPU") {
            steps {
                sh '''
                docker build \
                  --build-arg ENABLE_GPU=true \
                  -t $IMAGE_GPU .
                '''
            }
        }

        /* ================================
           20. Docker Run (CPU)
        ================================= */
        stage("Docker Run CPU") {
            steps {
                sh '''
                docker rm -f llm-cpu || true
                docker run -d \
                  -p 8777:8005 \
                  -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
                  -e MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME \
                  --name llm-cpu \
                  $IMAGE_CPU

                sleep 5
                curl -f http://localhost:8777/health
                '''
            }
        }

        /* ================================
           21. Docker Run (GPU)
        ================================= */
        stage("Docker Run GPU") {
            when {
                expression {
                    sh(script: 'nvidia-smi > /dev/null 2>&1', returnStatus: true) == 0
                }
            }
            steps {
                sh '''
                docker rm -f llm-gpu || true
                docker run -d \
                  --gpus all \
                  -p 8788:8005 \
                  -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
                  -e MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME \
                  --name llm-gpu \
                  $IMAGE_GPU

                sleep 5
                docker exec llm-gpu nvidia-smi
                curl -f http://localhost:8788/health
                '''
            }
        }

        /* ================================
           22. Archive Artifacts
        ================================= */
        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '''
                    mlruns/**,
                    uvicorn.log
                ''', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ LLM Customer Support Pipeline SUCCESS (CPU + GPU)"
        }
        failure {
            echo "❌ Pipeline FAILED – Check logs"
        }
        always {
            sh 'docker ps -a || true'
        }
    }
}
