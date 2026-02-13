"""
Authentication API module for Phase 4 system
Following Spec-4: Authentication & Authorization
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from backend.database.connection import get_db
from backend.mcp.users import create_user, authenticate_user, get_user_by_email
from backend.auth.utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from pydantic import BaseModel


router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/signup")
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    User registration endpoint
    Following Spec-4: Users can sign up with email and password
    Passwords are hashed as required
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    user = create_user(db, user_data.email, user_data.password)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "message": "User created successfully",
        "user_id": user.id,
        "email": user.email,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint
    Following Spec-4: Users can log in and receive a session or token
    """
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }