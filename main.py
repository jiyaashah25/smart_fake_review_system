"""
ReviewGuard AI - FastAPI Application Entry Point
"Trust Reviews. Detect Deception."
Provides high-performance REST APIs for NLP fake review detection, batch analysis,
and evaluation telemetry.
"""

import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import router as api_router
from api.schemas import HealthResponse
from api.exceptions import http_exception_handler, generic_exception_handler
from ml.predict import get_model

# Lifespan: Preload ML Model at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] Initializing ReviewGuard AI backend...")
    try:
        model_payload = get_model()
        model_name = model_payload.get("model_name", "ReviewGuard Classifier")
        print(f"[STARTUP] Successfully loaded model artifact: {model_name}")
    except Exception as e:
        print(f"[WARNING] Model artifact could not be loaded at startup: {e}")
        print("[WARNING] Predictions will fail until the model is trained with 'python -m ml.train_model'.")
    yield
    print("[SHUTDOWN] Shutting down ReviewGuard AI backend.")

app = FastAPI(
    title="ReviewGuard AI API",
    description="Smart Fake Review Detection System using NLP & Supervised Machine Learning.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API routes
app.include_router(api_router)

@app.get("/", tags=["System"])
def root_endpoint():
    """Returns application overview and operational status."""
    return {
        "name": "ReviewGuard AI",
        "tagline": "Trust Reviews. Detect Deception.",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs",
        "disclaimer": (
            "ReviewGuard AI provides automated predictions based on learned patterns in review data. "
            "Results are indicative and should not be treated as definitive proof of review fraud."
        )
    }

@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Returns service health status and ML model readiness without exposing filesystem internals."""
    model_loaded = False
    model_name = None
    try:
        artifact = get_model()
        model_loaded = True
        model_name = artifact.get("model_name", "Classifier")
    except Exception:
        model_loaded = False

    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        model_name=model_name,
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
