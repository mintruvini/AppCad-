import sqlite3
import os
from flask import Flask, render_template, request, redirect, flash
from auth import register_user
from models import init_db
from flask import session
from auth import login_user
from flask import request, redirect, render_template, flash, session
from werkzeug.utils import secure_filename
from utils.dwg_parser import analizar_dwg
from models_completo import crear_base_completa
crear_base_completa()
from utils.report_generator import generar_informe_pdf



app = Flask(__name__)
app.secret_key = 'clave-secreta-para-session'
init_db()  # Crear base si no existe

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        resultado = register_user(email, password)

        if resultado["ok"]:
            flash("Usuario registrado correctamente.")
            return redirect('/login')
        else:
            flash(resultado["error"])
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        resultado = login_user(email, password)

        if resultado["ok"]:
            session['user_id'] = resultado["user_id"]
            flash("Inicio de sesión exitoso.")
            return redirect('/dashboard')  # Página principal del usuario
        else:
            flash(resultado["error"])

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Opcional: obtener el email del usuario para mostrarlo
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("SELECT email FROM usuarios WHERE id = ?", (session['user_id'],))
        user = c.fetchone()
        conn.close()

        email = user[0] if user else None
        return render_template("dashboard.html", email=email)
    else:
        flash("Debés iniciar sesión primero.")
        return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect('/login')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'dwg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extension_permitida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/subir', methods=['GET', 'POST'])
def subir():
    # Verificar que el usuario esté logueado
    if 'user_id' not in session:
        flash("Debés iniciar sesión para subir archivos.")
        return redirect('/login')

    if request.method == 'POST':
        # Verificar que haya un archivo en el formulario
        if 'archivo' not in request.files:
            flash("No se seleccionó ningún archivo.")
            return redirect(request.url)

        archivo = request.files['archivo']

        # Verificar si se eligió un archivo
        if archivo.filename == '':
            flash("No seleccionaste un archivo.")
            return redirect(request.url)

        # Validar extensión y guardar archivo
        if archivo and extension_permitida(archivo.filename):
            nombre_seguro = secure_filename(archivo.filename)
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
            archivo.save(ruta)

            flash("Archivo cargado exitosamente.")
            return redirect('/dashboard')
        else:
            flash("Solo se permiten archivos DWG.")
            return redirect(request.url)
    

        # Luego de guardar archivo
            resultado = analizar_dwg(ruta)
            print("Capas detectadas:", resultado["capas_detectadas"])
            print("Datos extraídos:", resultado)


    # Si es GET, mostrar el formulario
    return render_template('subir.html')

@app.route('/historial')
def historial():
    if 'user_id' not in session:
        flash("Debés iniciar sesión.")
        return redirect('/login')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT nombre_archivo, fecha_subida, estado_procesamiento
        FROM archivo
        WHERE id_usuario = ?
        ORDER BY fecha_subida DESC
    ''', (session['user_id'],))
    archivos = c.fetchall()
    conn.close()

    return render_template("historial.html", archivos=archivos)

@app.route('/instructivos')
def instructivos():
    if 'user_id' not in session:
        flash("Debés iniciar sesión.")
        return redirect('/login')
    return render_template("instructivos.html")

@app.route('/notificaciones')
def notificaciones():
    if 'user_id' not in session:
        flash("Debés iniciar sesión.")
        return redirect('/login')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT tipo_mensaje, fecha_envio, contenido_resumen
        FROM log_notificaciones
        WHERE id_usuario = ?
        ORDER BY fecha_envio DESC
    ''', (session['user_id'],))
    notificaciones = c.fetchall()
    conn.close()

    return render_template("notificaciones.html", notificaciones=notificaciones)


def guardar_informe(cumple, observaciones, ruta_pdf, id_archivo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        INSERT INTO informe (cumple_normativa, observaciones, url_documento, id_archivo)
        VALUES (?, ?, ?, ?)
    ''', (
        cumple,
        observaciones,
        ruta_pdf,
        id_archivo
    ))
    conn.commit()
    conn.close()

@app.route('/informe/<int:id_archivo>')
def ver_informe(id_archivo):
    if 'user_id' not in session:
        flash("Debés iniciar sesión.")
        return redirect('/login')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT i.cumple_normativa, i.observaciones, i.url_documento, i.fecha_generacion, a.nombre_archivo
        FROM informe i
        JOIN archivo a ON a.id_archivo = i.id_archivo
        WHERE i.id_archivo = ?
    ''', (id_archivo,))
    datos = c.fetchone()
    conn.close()

    if not datos:
        flash("Informe no encontrado.")
        return redirect('/historial')

    cumple, observaciones, url_pdf, fecha, nombre_archivo = datos

    return render_template("informe.html", 
                           cumple=cumple,
                           observaciones=observaciones,
                           url_pdf=url_pdf,
                           fecha=fecha,
                           nombre_archivo=nombre_archivo)
