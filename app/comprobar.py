import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('iptv.db')
cursor = conn.cursor()

# Verificar si la tabla 'channels' existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='channels';")
table = cursor.fetchone()

if table:
    print("La tabla 'channels' existe.")
else:
    print("La tabla 'channels' no existe.")

# Cerrar la conexión
conn.close()