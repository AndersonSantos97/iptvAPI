from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from .models import Base, User, Channel
from .schemas import ChannelCreate, UserCreate
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.auth import router as auth_router
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
import httpx
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter

# Agregar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes, o especifica tu frontend (localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

security = HTTPBearer()
@app.get("/me")
def read_users_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {"token": credentials.credentials}

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
#agregar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], #origen permitido
    allow_credentials = True,
    allow_methods=["*"], # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  #Permitir todos los headers
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la IPTV API"}

# @app.get("/channels")
# def read_channels(db: Session = Depends(get_db)):
#     channels = db.query(Channel).all()
#     return channels

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    #verificar el usuario existe
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario registrado correctamente"}

@app.post("/token")
def login_for_access_token(user: UserCreate, db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
    
# @app.get("/channels")
# async def get_channels():
#     db = SessionLocal()
#     channels = db.query(Channel).all()
#     db.close()
#     return channels

@app.get("/channels")
def read_channels(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Channel).all()


@app.post("/channels/")
def create_channel(channel: ChannelCreate, db: Session = Depends(get_db)):
    db_channel = Channel(name=channel.name, url=channel.url)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

@router.get("/proxy")
async def proxy_m3u(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Lanza error si la respuesta es incorrecta
            return response.content  # Devuelve el contenido del archivo M3U
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error al acceder al M3U")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor")