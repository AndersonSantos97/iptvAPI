from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.models import User
from app.schemas import UserResponse, UserInDB, UserCreate
from typing import List
from sqlalchemy.orm import Session
from app.database import SessionLocal

#definir el SECRET para firmar el JWT
SECRET_KEY = "ESTRUCTURA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

fake_users_db = {}

#crear instancia de CryptContext pars encriptar contrasenas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#Utilizar OAuth2PasswordBearer para gestionar el flujo de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#funcion para encriptar las contrasenas
def get_password_hash(password: str):
    return pwd_context.hash(password)

#verificar si la contrasena es correcta
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#funcion para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#obtener usuario a partir de su nombre de usuario
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

#ruta para crear un nuevo usuario 
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    fake_users_db[user.username] = {"username": user.username, "hashed_password":get_password_hash(user.password), "preferred_channel":None}
    return UserResponse(username=user.username)

#ruta para obtener el JWT
@router.post("/token")
def login_for_access_token(user: UserCreate, db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

#ruta para obtener lo canales preferidos del usuario
@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(fake_users_db, username)
        if user is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    return user