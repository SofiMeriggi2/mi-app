import enum
from datetime import date
from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Genero(enum.Enum):
    masculino = "Masculino"
    femenino = "Femenino"
    otro = "Otro"
    no_decir = "Prefiero no decir"

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    nombre: Mapped[str | None] = mapped_column(String)
    apellido: Mapped[str | None] = mapped_column(String)
    genero: Mapped[Genero | None] = mapped_column(Enum(Genero))
    fecha_de_nacimiento: Mapped[date | None] = mapped_column(Date)