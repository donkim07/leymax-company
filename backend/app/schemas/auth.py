from typing import Dict, Any
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class LoginResponse(BaseModel):
    user: Dict[str, Any]
    token: Token 