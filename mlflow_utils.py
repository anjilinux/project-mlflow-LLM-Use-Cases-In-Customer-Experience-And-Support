import mlflow
import time

mlflow.set_tracking_uri("http://localhost:5555")
mlflow.set_experiment("llm-customer-support")

def log_llm_call(prompt, response, latency):
    with mlflow.start_run():
        mlflow.log_param("model_type", "llm")
        mlflow.log_metric("latency_sec", latency)
        mlflow.log_text(prompt, "prompt.txt")
        mlflow.log_text(response, "response.txt")
