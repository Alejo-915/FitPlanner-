from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from db import get_session
from models import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    fullname: str
    email: str
    password: str
    age: int
    goal: str

@router.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(Usuario).where(Usuario.correo == data.email)).first()
    if not user or user.contraseña != data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    return {"message": "Login exitoso", "user_id": user.id, "nombre": user.nombre}

@router.post("/register")
def register(data: RegisterRequest, session: Session = Depends(get_session)):
    existing_user = session.exec(select(Usuario).where(Usuario.correo == data.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")
    
    new_user = Usuario(
        nombre=data.fullname,
        correo=data.email,
        contraseña=data.password,
        edad=data.age,
        objetivo=data.goal
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "Registro exitoso", "user_id": new_user.id, "nombre": new_user.nombre}
