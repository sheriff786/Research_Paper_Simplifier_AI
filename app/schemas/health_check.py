"""
Health Check Schemas
Response models for health endpoints
"""
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    service: str
    version: str


class DetailedHealthResponse(BaseModel):
    """Detailed health check with system info"""
    status: str
    timestamp: datetime
    service: str
    version: str
    system: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T12:00:00",
                "service": "Research Paper Simplifier API",
                "version": "1.0.0",
                "system": {
                    "python_version": "3.11.0",
                    "platform": "Linux",
                }
            }
        }