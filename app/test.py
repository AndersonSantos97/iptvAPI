from app.database import SessionLocal
from app.models import Channel
from app.database import SessionLocal
from app.models import Channel

db = SessionLocal()

channels = db.query(Channel).all()
print("Canales en la base de datos:", channels)

db.close()
db = SessionLocal()
print(db.query(Channel).count())  # Debe mostrar cuántos canales hay en la BD
db.close()