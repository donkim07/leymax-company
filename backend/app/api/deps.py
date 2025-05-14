from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Cookie, Request
from sqlalchemy.orm import Session
import logging
from jose import JWTError

from app.core.security import decode_token
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.crud.crud_user import crud_user

# Session token cookie name
SESSION_TOKEN_NAME = "session_token"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG level

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_session_token(
    request: Request,
    session_token: Optional[str] = Cookie(None, alias=SESSION_TOKEN_NAME)
) -> str:
    """Get session token from cookie or Authorization header"""
    logger.debug("Attempting to get session token")
    logger.debug(f"Cookie token: {session_token}")
    logger.debug(f"Headers: {request.headers}")
    
    if session_token:
        logger.debug("Found token in cookie")
        return session_token
    
    # Try to get token from Authorization header
    auth_header = request.headers.get("Authorization")
    logger.debug(f"Authorization header: {auth_header}")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        logger.debug(f"Found token in Authorization header: {token[:10]}...")
        return token
    
    logger.debug("No token found in cookie or Authorization header")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )

def get_current_user(
    db: Session = Depends(get_db),
    session_token: str = Depends(get_session_token)
) -> User:
    """Get current user from JWT token"""
    try:
        logger.debug(f"Getting user from JWT token: {session_token[:10]}...")
        payload = decode_token(session_token)
        logger.debug(f"Token payload: {payload}")
        
        # Try to get user_id from either sub or user_id
        user_id = None
        if "sub" in payload:
            user_id = int(payload["sub"])
            logger.debug(f"Found user_id in sub: {user_id}")
        elif "user_id" in payload:
            user_id = int(payload["user_id"])
            logger.debug(f"Found user_id in user_id: {user_id}")
            
        if not user_id:
            logger.error("No user ID found in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format"
            )
        
        user = crud_user.get(db, id=user_id)
        if not user:
            logger.debug(f"User {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # Only verify essential token data
        if payload.get("email") and payload.get("email") != user.email:
            logger.error(f"Token email mismatch: {payload.get('email')} != {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token data mismatch"
            )
            
        logger.debug(f"Successfully retrieved user: {user.email}")
        return user
    except JWTError as e:
        logger.error(f"Invalid JWT token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    except ValueError as e:
        logger.error(f"Value error in token processing: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user and verify they are active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Get current user and verify they are an admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_store_manager(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Get current user and verify they are an admin or manager"""
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
