from app.database import engine, Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Verificar si la tabla 'channels' se ha creado
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()

if "channels" in tables:
    print("La tabla 'channels' se ha creado correctamente.")
else:
    print("La tabla 'channels' no se ha creado.")

print("Base de datos y tablas creadas correctamente")
    