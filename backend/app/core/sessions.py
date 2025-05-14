import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import time

# In-memory sessions store (replace with Redis/database in production)
# Structure: {session_id: {user_id: int, expires_at: float, data: Dict}}
sessions: Dict[str, Dict[str, Any]] = {}

def create_session(user_id: int, data: Dict[str, Any] = None, expires_days: int = 30) -> str:
    """
    Create a new session for a user
    
    Args:
        user_id: The ID of the user
        data: Additional session data
        expires_days: Number of days before the session expires
        
    Returns:
        str: The session token
    """
    # Generate a unique session token
    session_token = secrets.token_hex(32)
    
    # Calculate expiration time
    expires_at = time.time() + (expires_days * 24 * 60 * 60)
    
    # Store session
    sessions[session_token] = {
        "user_id": user_id,
        "expires_at": expires_at,
        "data": data or {}
    }
    
    return session_token

def get_session(session_token: str) -> Optional[Dict[str, Any]]:
    """
    Get session data if valid
    
    Args:
        session_token: The session token
        
    Returns:
        Optional[Dict]: Session data or None if invalid/expired
    """
    session = sessions.get(session_token)
    
    if not session:
        return None
        
    # Check if session has expired
    if session["expires_at"] < time.time():
        delete_session(session_token)
        return None
        
    return session

def delete_session(session_token: str) -> None:
    """
    Delete a session
    
    Args:
        session_token: The session token to delete
    """
    if session_token in sessions:
        del sessions[session_token]

def get_user_sessions(user_id: int) -> Dict[str, Dict[str, Any]]:
    """
    Get all sessions for a user
    
    Args:
        user_id: The user ID
        
    Returns:
        Dict: All active sessions for the user
    """
    return {
        token: session 
        for token, session in sessions.items() 
        if session["user_id"] == user_id and session["expires_at"] >= time.time()
    }

def delete_all_user_sessions(user_id: int) -> None:
    """
    Delete all sessions for a user
    
    Args:
        user_id: The user ID
    """
    tokens_to_delete = [
        token for token, session in sessions.items() 
        if session["user_id"] == user_id
    ]
    
    for token in tokens_to_delete:
        delete_session(token) 