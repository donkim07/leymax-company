from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def create_access_token(
    subject: Union[str, Any],
    data: dict = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token
    """
    try:
        to_encode = {}
        if data:
            # Convert any datetime objects to ISO format strings
            for key, value in data.items():
                if isinstance(value, datetime):
                    to_encode[key] = value.isoformat()
                else:
                    to_encode[key] = value
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=30)
        
        to_encode.update({
            "exp": int(expire.timestamp()),  # Convert to Unix timestamp
            "sub": str(subject),
            "iat": int(datetime.utcnow().timestamp())  # Convert to Unix timestamp
        })
        
        logger.debug(f"Creating token with payload: {to_encode}")
        token = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm="HS256"
        )
        logger.debug("Token created successfully")
        return token
    except Exception as e:
        logger.error(f"Error creating token: {str(e)}")
        raise

def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token
    """
    try:
        logger.debug("Attempting to decode token")
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        logger.debug(f"Token decoded successfully: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError as e:
        logger.error(f"JWT error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)
