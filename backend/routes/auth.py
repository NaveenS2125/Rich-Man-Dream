from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from ..database.connection import users_collection
from ..auth.jwt_handler import verify_password, create_access_token
from ..auth.middleware import get_current_user_email, get_current_user_data
from ..models.user import UserResponse
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: str
    user: UserResponse
    message: str = "Login successful"


class ErrorResponse(BaseModel):
    success: bool = False
    error: str


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """Authenticate user and return JWT token."""
    
    # Find user by email
    user_doc = await users_collection.find_one({"email": login_data.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user_doc["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    token_data = {
        "sub": user_doc["email"],
        "user_id": str(user_doc["_id"]),
        "name": user_doc["name"],
        "role": user_doc["role"]
    }
    access_token = create_access_token(token_data)
    
    # Prepare user response
    user_response = UserResponse(
        id=str(user_doc["_id"]),
        name=user_doc["name"],
        email=user_doc["email"],
        role=user_doc["role"],
        avatar=user_doc.get("avatar")
    )
    
    return LoginResponse(
        success=True,
        token=access_token,
        user=user_response,
        message="Login successful"
    )


@router.post("/logout")
async def logout():
    """Logout user (client should remove token)."""
    return {"success": True, "message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_email: str = Depends(get_current_user_email)):
    """Get current user information."""
    
    user_doc = await users_collection.find_one({"email": user_email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user_doc["_id"]),
        name=user_doc["name"],
        email=user_doc["email"],
        role=user_doc["role"],
        avatar=user_doc.get("avatar")
    )