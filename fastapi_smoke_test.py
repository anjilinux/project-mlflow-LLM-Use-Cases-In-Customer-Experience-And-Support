# fastapi_smoke_test.py
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Create a tiny FastAPI app
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Run a quick test using TestClient
if __name__ == "__main__":
    client = TestClient(app)
    response = client.get("/health")
    if response.status_code == 200 and response.json() == {"status": "ok"}:
        print("✅ FastAPI Smoke Test Passed")
    else:
        print("❌ FastAPI Smoke Test Failed")
