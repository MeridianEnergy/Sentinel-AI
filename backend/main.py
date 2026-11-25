
from fastapi import FastAPI

app = FastAPI(
    title="SENTINEL AI",
    description="AI-assisted Emergency Operations and Coordination Platform",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "system": "SENTINEL AI",
        "status": "online",
        "message": "SENTINEL AI backend is operational."
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "SENTINEL AI"
    }
