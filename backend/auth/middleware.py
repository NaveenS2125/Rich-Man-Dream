from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt_handler import decode_token, verify_token

security = HTTPBearer()


async def get_current_user_email(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user email from JWT token."""
    token = credentials.credentials
    email = decode_token(token)
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return email


async def verify_admin_role(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify that the current user has admin role."""
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    role = payload.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    return payload


async def get_current_user_data(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user data from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


# Optional auth for endpoints that can work with or without auth
async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))) -> Optional[dict]:
    """Get current user data if token is provided, otherwise return None."""
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = verify_token(token)
    return payload