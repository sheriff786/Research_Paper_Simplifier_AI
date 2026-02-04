"""
Health Check Endpoints
API endpoints for service health monitoring
"""
from fastapi import APIRouter
from datetime import datetime
import platform
import sys
from app.config import settings
from app.schemas.health import HealthResponse, DetailedHealthResponse


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Simple health check endpoint
    Returns basic service status
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


@router.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """
    Detailed health check endpoint
    Returns service status with system information
    """
    return DetailedHealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        system={
            "python_version": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
    )


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint
    Quick connectivity test
    """
    return {"ping": "pong", "timestamp": datetime.utcnow().isoformat()}