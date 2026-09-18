import enum
from sqlalchemy import Column, Integer, String, Date, Enum
from database import Base

class Genero(enum.Enum):
    masculino = "Masculino"
    femenino = "Femenino"
    otro = "Otro"
    no_decir = "Prefiero no decir"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    genero = Column(Enum(Genero), nullable=False)
    fecha_de_nacimiento = Column(Date, nullable=False)