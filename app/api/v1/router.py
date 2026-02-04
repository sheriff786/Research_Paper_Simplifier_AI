"""
API v1 Router
Main router that includes all API endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health


# Create main API router
api_router = APIRouter()


# Include all endpoint routers
api_router.include_router(
    health.router,
    tags=["Health"],
)


# You can add more routers here as you build them
# api_router.include_router(papers.router, prefix="/papers", tags=["Papers"])
# api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])