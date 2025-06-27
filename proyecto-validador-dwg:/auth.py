import sqlite3
import bcrypt
import re

def register_user(email, password):
    # Validaciones básicas
    if not email or not password:
        return {"ok": False, "error": "Todos los campos son obligatorios."}

    if len(password) < 8:
        return {"ok": False, "error": "La contraseña debe tener al menos 8 caracteres."}

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"ok": False, "error": "Formato de correo inválido."}

    # Encriptar contraseña
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Conectar a la base de datos
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Verificar si el email ya está registrado
    c.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    if c.fetchone():
        conn.close()
        return {"ok": False, "error": "Ese email ya está registrado."}

    # Insertar nuevo usuario
    c.execute("INSERT INTO usuarios (email, password) VALUES (?, ?)", (email, hashed))
    conn.commit()
    conn.close()

    return {"ok": True}

def login_user(email, password):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Buscar al usuario por email
    c.execute("SELECT id, password FROM usuarios WHERE email = ?", (email,))
    user = c.fetchone()

    if not user:
        return {"ok": False, "error": "El usuario no existe."}

    user_id, hashed_password = user

    # Comparar contraseñas
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return {"ok": True, "user_id": user_id}
    else:
        return {"ok": False, "error": "Contraseña incorrecta."}

