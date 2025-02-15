from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    username: str
    preferred_chanel: Optional[str] = None
    
    class Config:
        from_attributes = True

# Esquema para usuario con contraseña (para autenticación)
class UserInDB(UserResponse):
    hashed_password:str
    
    
class ChannelCreate(BaseModel):
    name: str
    url: str