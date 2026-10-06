from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario, Genero
import schemas
import auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de FastAPI"}


@app.post("/sign-up", response_model=schemas.UsuarioResponse)
def sign_up(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    nuevo_usuario = Usuario (
        email = usuario.email,
        password_hash = auth.hash_password(usuario.password)
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario


@app.post("/login", response_model=schemas.Token)
def login(credenciales: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credenciales.email).first()

    if not usuario or not auth.verify_password(credenciales.password, str(usuario.password_hash)):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    access_token = auth.create_access_token(data={"sub": usuario.email})

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UsuarioResponse)
def leer_usuario_actual(usuario_actual: Usuario = Depends(auth.get_current_user)):
    return usuario_actual

@app.put("/me", response_model=schemas.UsuarioResponse)
def completar_perfil(
    perfil: schemas.UsuarioPerfil,
    usuario_actual: Usuario = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    usuario_actual.nombre = perfil.nombre
    usuario_actual.apellido = perfil.apellido
    usuario_actual.genero = perfil.genero
    usuario_actual.fecha_de_nacimiento = perfil.fecha_de_nacimiento
    
    db.commit()
    db.refresh(usuario_actual)
    
    return usuario_actual