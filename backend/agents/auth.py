"""JWT Authentication System for EEFai"""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
import secrets

from database import get_mongo_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()

# JWT Configuration
JWT_SECRET = secrets.token_urlsafe(32)  # In production, use env var
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


@router.post("/register")
async def register(email: str, password: str, name: str):
    """Register new user with email and password"""
    try:
        db = get_mongo_db()
        
        # Check if user exists
        existing = await db.users.find_one({"email": email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Create user
        user = {
            "email": email,
            "name": name,
            "password_hash": password_hash,
            "role": "user",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "active": True
        }
        
        await db.users.insert_one(user)
        
        # Generate JWT
        token = generate_jwt(email, "user")
        
        logger.info(f"User registered: {email}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "email": email,
            "name": name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(email: str, password: str):
    """Login with email and password"""
    try:
        db = get_mongo_db()
        
        # Find user
        user = await db.users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Check if active
        if not user.get("active", True):
            raise HTTPException(status_code=403, detail="Account disabled")
        
        # Generate JWT
        token = generate_jwt(email, user.get("role", "user"))
        
        logger.info(f"User logged in: {email}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "email": email,
            "name": user.get("name")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh JWT token"""
    try:
        # Verify current token
        payload = verify_jwt(credentials.credentials)
        
        # Generate new token
        new_token = generate_jwt(payload["email"], payload["role"])
        
        return {
            "access_token": new_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout (token revocation would go here)"""
    try:
        # In production, add token to revocation list in Redis
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    try:
        payload = verify_jwt(credentials.credentials)
        
        db = get_mongo_db()
        user = await db.users.find_one({"email": payload["email"]}, {"_id": 0, "password_hash": 0})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def generate_jwt(email: str, role: str) -> str:
    """Generate JWT token for user"""
    payload = {
        "email": email,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.now(timezone.utc)
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user_email(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency to get current user email from JWT"""
    payload = verify_jwt(credentials.credentials)
    return payload["email"]


async def require_role(required_role: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to check user role"""
    payload = verify_jwt(credentials.credentials)
    
    if payload["role"] != required_role and payload["role"] != "system_admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return payload["email"]
