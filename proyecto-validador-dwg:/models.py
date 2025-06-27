import sqlite3

# Crear tabla de usuarios
def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Crear tabla de archivos DWG
def crear_tabla_archivo():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS archivo (
            id_archivo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            ruta_archivo TEXT NOT NULL,
            fecha_subida TEXT DEFAULT CURRENT_TIMESTAMP,
            estado_procesamiento TEXT DEFAULT 'pendiente',
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

# Crear tabla de notificaciones
def crear_tabla_notificaciones():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS log_notificaciones (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_mensaje TEXT,
            fecha_envio TEXT DEFAULT CURRENT_TIMESTAMP,
            estado_envio TEXT,
            contenido_resumen TEXT,
            id_usuario INTEGER,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

