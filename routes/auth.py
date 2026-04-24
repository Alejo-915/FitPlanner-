from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional
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
    peso: Optional[float] = None
    altura: Optional[float] = None
    # Nuevos campos
    limitaciones: Optional[List[str]] = []   # lista de limitaciones físicas
    meses_sin_ejercicio: Optional[int] = 0
    dias_semana: Optional[int] = 3


@router.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(Usuario).where(Usuario.correo == data.email)).first()
    if not user or user.contraseña != data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return {
        "message": "Login exitoso",
        "user_id": user.id,
        "nombre": user.nombre,
        "objetivo": user.objetivo,
        "nivel_condicion": user.nivel_condicion,
    }


@router.post("/register")
def register(data: RegisterRequest, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(Usuario).where(Usuario.correo == data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    # Convertir lista de limitaciones a string separado por comas
    limitaciones_str = ",".join(data.limitaciones) if data.limitaciones else None

    # Nivel inicial según tiempo sin ejercicio
    if data.meses_sin_ejercicio == 0:
        nivel = "intermedio"
    elif data.meses_sin_ejercicio <= 3:
        nivel = "principiante"
    else:
        nivel = "principiante"

    new_user = Usuario(
        nombre=data.fullname,
        correo=data.email,
        contraseña=data.password,
        edad=data.age,
        objetivo=data.goal,
        peso=data.peso,
        altura=data.altura,
        limitaciones=limitaciones_str,
        meses_sin_ejercicio=data.meses_sin_ejercicio,
        dias_semana=data.dias_semana,
        nivel_condicion=nivel,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {
        "message": "Registro exitoso",
        "user_id": new_user.id,
        "nombre": new_user.nombre,
        "nivel_condicion": new_user.nivel_condicion,
    }