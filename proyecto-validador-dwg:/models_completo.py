import sqlite3

def crear_base_completa():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
            estado_cuenta TEXT DEFAULT 'activo'
        )
    ''')

    # Tabla de archivos
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

    # Tabla de informes
    c.execute('''
        CREATE TABLE IF NOT EXISTS informe (
            id_informe INTEGER PRIMARY KEY AUTOINCREMENT,
            cumple_normativa BOOLEAN NOT NULL,
            observaciones TEXT,
            url_documento TEXT,
            fecha_generacion TEXT DEFAULT CURRENT_TIMESTAMP,
            id_archivo INTEGER NOT NULL,
            FOREIGN KEY (id_archivo) REFERENCES archivo (id_archivo)
        )
    ''')

    # Tabla de normativas
    c.execute('''
        CREATE TABLE IF NOT EXISTS normativa (
            id_normativa INTEGER PRIMARY KEY AUTOINCREMENT,
            zona TEXT,
            parametro TEXT,
            valor_maximo REAL,
            unidad TEXT,
            observaciones TEXT
        )
    ''')

    # Tabla de trámites
    c.execute('''
        CREATE TABLE IF NOT EXISTS tramite (
            id_tramite INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_inicio TEXT DEFAULT CURRENT_TIMESTAMP,
            estado_tramite TEXT,
            comentarios_municipales TEXT,
            id_informe INTEGER,
            FOREIGN KEY (id_informe) REFERENCES informe (id_informe)
        )
    ''')

    # Tabla de notificaciones
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
