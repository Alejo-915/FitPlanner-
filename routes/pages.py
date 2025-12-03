from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/home")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.get("/home/user")
def user_home(request: Request):
    return templates.TemplateResponse("user/home.html", {"request": request})

@router.get("/home/admin")
def admin_home(request: Request):
    return templates.TemplateResponse("admin/home.html", {"request": request})

@router.get("/admin/usuarios")
def admin_usuarios(request: Request):
    return templates.TemplateResponse("admin/usuarios.html", {"request": request})

@router.get("/admin/ejercicios")
def admin_ejercicios(request: Request):
    return templates.TemplateResponse("admin/ejercicios.html", {"request": request})

@router.get("/admin/rutinas")
def admin_rutinas(request: Request):
    return templates.TemplateResponse("admin/rutinas.html", {"request": request})