import re
from app.database import SessionLocal
from app.models import Channel

# Función para parsear el archivo .m3u
def parse_m3u(file_path):
    channels = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                match = re.search(r'tvg-name="([^"]+)"', lines[i])
                name = match.group(1) if match else "Canal Desconocido"
                url = lines[i + 1].strip()
                channels.append({"name": name, "url": url})
    return channels

# Cargar los canales desde playlist.m3u
playlist_file = "playlist.m3u"
channels_data = parse_m3u(playlist_file)

# Conectar a la base de datos
db = SessionLocal()

# Verificar si hay canales en la BD
if not db.query(Channel).first():
    print("No hay canales en la base de datos. Insertando desde playlist.m3u...")

    for channel in channels_data:
        new_channel = Channel(name=channel["name"], url=channel["url"])
        db.add(new_channel)

    db.commit()
    print("Canales insertados correctamente desde playlist.m3u.")
else:
    print("Los canales ya existen en la base de datos.")

db.close()