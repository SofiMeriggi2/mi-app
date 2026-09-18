from database import Base, engine
from models import Usuario

Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")