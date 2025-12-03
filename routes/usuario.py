from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/")
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.get("/")
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario).where(Usuario.activo == True)).all()

@router.get("/{id}")
def obtener_usuario(id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, id)
    if not usuario or not usuario.activo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.patch("/{id}")
def actualizar_usuario(id: int, datos: Usuario, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(usuario, key, value)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.delete("/{id}")
def eliminar_usuario(id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.activo = False
    session.add(usuario)
    session.commit()
    return {"mensaje": "Usuario desactivado correctamente"}
