"""
ReviewGuard AI - Custom API Exceptions and Error Handlers
Provides clean, secure error responses without exposing server paths or raw tracebacks.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class ModelNotLoadedException(HTTPException):
    def __init__(self, detail: str = "ML model artifact is not loaded. Train the model using 'python -m ml.train_model'."):
        super().__init__(status_code=503, detail=detail)

class InvalidReviewInputException(HTTPException):
    def __init__(self, detail: str = "Invalid review text provided."):
        super().__init__(status_code=400, detail=detail)

class BatchProcessingException(HTTPException):
    def __init__(self, detail: str = "Error processing batch CSV upload."):
        super().__init__(status_code=422, detail=detail)

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing the request.",
            "status_code": 500
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request Error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )
