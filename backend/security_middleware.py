"""Security middleware for rate limiting and headers"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from database import get_redis
import time
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://assets.emergent.sh https://us.i.posthog.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:;"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting using Redis or in-memory fallback"""
    
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.memory_cache = {}  # Fallback if Redis unavailable
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health check
        if request.url.path in ["/api/", "/api"]:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        
        # Try Redis first
        redis = get_redis()
        if redis:
            try:
                key = f"ratelimit:{client_ip}"
                current = await redis.get(key)
                
                if current is None:
                    await redis.setex(key, self.window_seconds, 1)
                    return await call_next(request)
                
                count = int(current)
                if count >= self.max_requests:
                    logger.warning(f"Rate limit exceeded for {client_ip}")
                    raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
                
                await redis.incr(key)
                return await call_next(request)
                
            except HTTPException:
                raise
            except Exception as e:
                logger.warning(f"Redis rate limit error: {e}, using memory fallback")
        
        # Fallback to in-memory
        now = time.time()
        
        # Clean old entries
        self.memory_cache = {
            ip: (count, timestamp) 
            for ip, (count, timestamp) in self.memory_cache.items()
            if now - timestamp < self.window_seconds
        }
        
        if client_ip in self.memory_cache:
            count, timestamp = self.memory_cache[client_ip]
            if count >= self.max_requests:
                raise HTTPException(status_code=429, detail="Too many requests")
            self.memory_cache[client_ip] = (count + 1, timestamp)
        else:
            self.memory_cache[client_ip] = (1, now)
        
        return await call_next(request)
