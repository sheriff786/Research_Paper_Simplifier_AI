"""
Custom Middleware
Request logging and processing
"""
import time
from fastapi import Request
from app.config import settings


async def log_requests(request: Request, call_next):
    """
    Log all incoming requests with timing
    """
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add custom header
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log request (only in debug mode)
    if settings.DEBUG:
        print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
    
    return response