from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field, PastDate
from models import Genero

class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str

class UsuarioResponse(BaseModel):
    id: int
    email: str
    nombre: str | None = None
    apellido: str | None = None
    genero: Genero | None = None
    fecha_de_nacimiento: date | None = None
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioPerfil(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    nombre: str = Field(min_length=1, max_length=50)
    apellido: str = Field(min_length=1, max_length=50)
    genero: Genero
    fecha_de_nacimiento: PastDate = Field(ge=date(1900, 1, 1))
    