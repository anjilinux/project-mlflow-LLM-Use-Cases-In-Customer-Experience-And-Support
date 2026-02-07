pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv_llm"
        OPENAI_API_KEY = "dummy"  // safe for testing
    }

    stages {

        stage('Setup Python Environment') {
            steps {
                echo "⚡ Setting up virtual environment..."
                sh '''
                #!/bin/bash
                # Only create venv if it doesn't exist
                if [ ! -d "$VENV_DIR" ]; then
                    python3 -m venv "$VENV_DIR"
                fi

                # Activate venv
                . "$VENV_DIR/bin/activate"

                # Upgrade pip and install packages only if not already installed
                #pip install --upgrade pip
                #pip install langchain faiss-cpu pytest fastapi[all] || true
                '''
            }
        }

        stage('Lint Python Files') {
            steps {
                echo "🔍 Linting Python files..."
                sh '''
                . "$VENV_DIR/bin/activate"
                python -m py_compile llm_client.py rag.py vector_store.py prompts.py config.py monitor.py logger.py schema.py || true
                '''
            }
        }

        stage('Run Pytests') {
            steps {
                echo "🧪 Running tests..."
                sh '''
                . "$VENV_DIR/bin/activate"
                pytest test_dummy.py -v || true
                '''
            }
        }

        stage('Run Vector Store Script') {
            steps {
                echo "🚀 Running vector_store.py..."
                sh '''
                . "$VENV_DIR/bin/activate"
                python vector_store.py || true
                '''
            }
        }

        stage('FastAPI Smoke Test') {
            steps {
                echo "🧪 FastAPI Smoke Test..."
                sh '''
                . "$VENV_DIR/bin/activate"
                python fastapi_smoke_test.py || true
                '''
            }
        }

    }

    post {
        always {
            echo "Pipeline finished!"
        }
    }
}





















































































































// pipeline {
//     agent any

//     environment {
//         // Python
//         VENV_NAME = "venv"
//         APP_PORT = "8005"
//         PYTHONPATH = "${WORKSPACE}"

//         // MLflow
//         MLFLOW_TRACKING_URI = "http://localhost:5555"
//         MLFLOW_EXPERIMENT_NAME = "llm-customer-support"

//         // Docker Images
//         IMAGE_CPU = "llm-customer-support:cpu"
//         IMAGE_GPU = "llm-customer-support:gpu"
//     }

//     options {
//         timeout(time: 90, unit: 'MINUTES')
//         timestamps()
//     }

//     stages {

//         /* ================================
//            1. Checkout
//         ================================= */
//         stage("Checkout Code") {
//             steps {
//                 git branch: "master",
//                     url: "https://github.com/anjilinux/project-mlflow-LLM-Use-Cases-In-Customer-Experience-And-Support.git"
//             }
//         }

//         /* ================================
//            2. Load Environment Variables
//         ================================= */
//         stage("Load Environment Variables") {
//             steps {
//                 sh '''
//                 if [ -f .env ]; then
//                     export $(grep -v '^#' .env | xargs)
//                     echo "✅ .env loaded"
//                 else
//                     echo "⚠️ .env not found"
//                 fi
//                 '''
//             }
//         }

//         /* ================================
//            3. Setup Python Virtual Environment
//         ================================= */
// stage("Setup Virtual Environment") {
//     steps {
//         sh '''
//         python3 -m venv $VENV_NAME
//         . $VENV_NAME/bin/activate

//         pip install -r requirements.txt
//         pip install pytest pytest-cov flake8 black
//         '''
//     }
// }

//         /* ================================
//            4. Validate Knowledge Base
//         ================================= */
//         stage("Validate sample_faqs.txt") {
//             steps {
//                 sh '''
//                 test -f sample_faqs.txt
//                 echo "✅ sample_faqs.txt found"
//                 '''
//             }
//         }

//         /* ================================
//            5. Lint
//         ================================= */
//         stage("Lint") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate

//                 FILES="
//                 app.py
//                 llm_client.py
//                 rag.py
//                 vector_store.py
//                 prompts.py
//                 config.py
//                 monitor.py
//                 logger.py
//                 ingest_data.py
//                 schema.py
//                 "

//                 for f in $FILES; do
//                   if [ -f "$f" ]; then
//                     echo "🔍 Linting $f"
//                     python -m py_compile "$f"
//                   else
//                     echo "⚠️ Skipping missing file: $f"
//                   fi
//                 done
//                 '''
//             }
//         }

//         /* ================================
//            6. Unit Tests
//         ================================= */
//         stage("Pytests") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 pytest  test_dummy.py  -v
//                 '''
//             }
//         }

//         /* ================================
//            7. Schema Validation
//         ================================= */
//         stage("Schema Validation") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 python schema.py
//                 '''
//             }
//         }

//         /* ================================
//            8. LangChain Modern Sanity Check
//         ================================= */
//         stage("LangChain Modern Sanity Check") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 python - <<EOF
// from langchain_openai import OpenAIEmbeddings, ChatOpenAI
// print("✅ Modern LangChain imports OK")
// EOF
//                 '''
//             }
//         }




//         /* ================================
//            9. Vector Store
//         ================================= */
 

// stage('Vector Store') {
//     steps {
//        sh ". $VENV_NAME/bin/activate"
//        sh "pip install -U langchain-openai langchain-community faiss-cpu"
//         sh 'pip install langchain-openai'

//         sh '''
//         #!/bin/bash
//         set -e  # Fail fast if any command fails

//         echo "🔹 Activating virtual environment"
//         . venv/bin/activate

//         echo "🔹 Installing requirements"
      
//         pip install -r requirements.txt

//         echo "🔹 Running vector_store.py"
//         python vector_store.py
//         '''
//     }
// }



//         /* ================================
//            10. Prompts
//         ================================= */
//         stage("Prompts") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 python - <<EOF
// import prompts
// print("✅ prompts loaded")
// EOF
//                 '''
//             }
//         }

//         /* ================================
//            11. Monitor
//         ================================= */
//         stage("Monitor") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 python - <<EOF
// import monitor
// print("✅ monitor loaded")
// EOF
//                 '''
//             }
//         }

//         /* ================================
//            12. Logger
//         ================================= */
//         stage("Logger") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 python - <<EOF
// import logger
// print("✅ logger loaded")
// EOF
//                 '''
//             }
//         }

//         /* ================================
//            13. Config + MLflow
//         ================================= */
//         stage("Config & MLflow") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
//                 export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
//                 python - <<EOF
// import config
// print("✅ config + MLflow loaded")
// EOF
//                 '''
//             }
//         }

//         /* ================================
//            14. LLM Client
//         ================================= */
//         stage("LLM Client") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 python - <<EOF
// import llm_client
// print("✅ llm_client loaded")
// EOF
//                 '''
//             }
//         }

//         /* ================================
//            15. Ingest Data
//         ================================= */
//         stage("Ingest Data") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 if [ -f ingest_data.py ]; then
//                     python ingest_data.py
//                 else
//                     echo "⚠️ ingest_data.py missing, skipping"
//                 fi
//                 '''
//             }
//         }

//         /* ================================
//            16. RAG Pipeline
//         ================================= */
//         stage("RAG Pipeline") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 if [ -f rag.py ]; then
//                     python rag.py
//                 else
//                     echo "⚠️ rag.py missing, skipping"
//                 fi
//                 '''
//             }
//         }

//         /* ================================
//            17. FastAPI Import
//         ================================= */
//         stage("FastAPI Import") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 python - <<EOF
// from app import app
// print("✅ FastAPI app import OK")
// EOF
//                 '''
//             }
//         }

//         /* ================================
//            18. FastAPI Smoke Test (Local)
//         ================================= */
//         stage("FastAPI Smoke Test") {
//             steps {
//                 sh '''
//                 . $VENV_NAME/bin/activate
//                 nohup uvicorn app:app \
//                   --host 0.0.0.0 \
//                   --port $APP_PORT > uvicorn.log 2>&1 &

//                 sleep 5
//                 curl -f http://localhost:$APP_PORT/health
//                 pkill -f "uvicorn app:app" || true
//                 '''
//             }
//         }

//         /* ================================
//            19. Docker Build (CPU)
//         ================================= */
//         stage("Docker Build CPU") {
//             steps {
//                 sh '''
//                 docker build -t $IMAGE_CPU .
//                 '''
//             }
//         }

//         /* ================================
//            20. Docker Build (GPU)
//         ================================= */
//         stage("Docker Build GPU") {
//             steps {
//                 sh '''
//                 docker build --build-arg ENABLE_GPU=true -t $IMAGE_GPU .
//                 '''
//             }
//         }

//         /* ================================
//            21. Docker Run (CPU)
//         ================================= */
//         stage("Docker Run CPU") {
//             steps {
//                 sh '''
//                 docker rm -f llm-cpu || true
//                 docker run -d \
//                   -p 8777:8005 \
//                   -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
//                   -e MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME \
//                   --name llm-cpu \
//                   $IMAGE_CPU

//                 sleep 5
//                 curl -f http://localhost:8777/health
//                 '''
//             }
//         }

//         /* ================================
//            22. Docker Run (GPU)
//         ================================= */
//         stage("Docker Run GPU") {
//             when {
//                 expression { sh(script: 'nvidia-smi > /dev/null 2>&1', returnStatus: true) == 0 }
//             }
//             steps {
//                 sh '''
//                 docker rm -f llm-gpu || true
//                 docker run -d \
//                   --gpus all \
//                   -p 8788:8005 \
//                   -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
//                   -e MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME \
//                   --name llm-gpu \
//                   $IMAGE_GPU

//                 sleep 5
//                 docker exec llm-gpu nvidia-smi
//                 curl -f http://localhost:8788/health
//                 '''
//             }
//         }

//         /* ================================
//            23. Archive Artifacts
//         ================================= */
//         stage("Archive Artifacts") {
//             steps {
//                 archiveArtifacts artifacts: '''
//                     mlruns/**,
//                     uvicorn.log
//                 ''', fingerprint: true
//             }
//         }

//     }

//     post {
//         success { echo "✅ LLM Customer Support Pipeline SUCCESS (CPU + GPU)" }
//         failure { echo "❌ Pipeline FAILED – Check logs" }
//         always { sh 'docker ps -a || true' }
//     }
// }
