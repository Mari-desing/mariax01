# Importamos las librerías
from flask import Flask, render_template, request
import sqlite3
import os

# --- Definir rutas absolutas para templates y static ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Instanciamos en app la clase que recibe como parámetro la aplicación
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

# --- Definir la ruta absoluta para la base de datos ---
db_path = os.path.join(BASE_DIR, "data", "viajes.db")

# Decorador que asocia una URL con una función Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/precios_viajes')
def precios_viajes():
    return render_template('precios_viajes.html')

@app.route('/contacto', methods=("POST", "GET"))
def contacto():
    if request.method == "POST":
        nombre_completo = request.form['nombre_completo']
        correo_electronico = request.form['correo_electronico']
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']

        conexion = sqlite3.connect(db_path)
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO contacto (nombre_completo, correo_electronico, asunto, mensaje) VALUES (?,?,?,?)",
            (nombre_completo, correo_electronico, asunto, mensaje)
        )
        conexion.commit()
        conexion.close()

    return render_template('contacto.html')

@app.route('/confirmacion')
def confirmacion():
    from datetime import datetime
    import random

    nombre = request.args.get('nombre')
    correo = request.args.get('correo')
    paquete = request.args.get('paquete')

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    numero_factura = f"FAC-{random.randint(1000, 9999)}"

    precios = {
        "muralla": "30$ - 50$",
        "prohibida": "40$",
        "terracota": "20$ - 48$",
        "crucero": "90$ - 115$",
        "ciqikou": "56$ - 60$",
        "templo cielo": "40$ - 60$",
        "jardin": "30$",
        "montaña": "55$"
    }

    nombres_paquetes = {
        "muralla": "Gran Muralla China",
        "prohibida": "Ciudad Prohibida",
        "terracota": "Ejército de Terracota",
        "crucero": "Río Li (Crucero)",
        "ciqikou": "Ciqikou",
        "templo cielo": "Templo del Cielo",
        "jardin": "Jardín Yuyuan",
        "montaña": "Montaña Tianmen"
    }

    destino = nombres_paquetes.get(paquete, "Destino desconocido")
    precio = precios.get(paquete, "No disponible")

    return render_template(
        'confirmacion.html',
        nombre=nombre,
        correo=correo,
        paquete=destino,
        precio=precio,
        fecha=fecha,
        numero_factura=numero_factura
    )

@app.route('/ver_precio')
def ver_precio():
    return render_template('ver_precio.html')

@app.route('/informacion')
def informacion():
    return render_template('Informacion.html')

@app.route('/formu', methods=['GET', 'POST'])
def formu():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre_completo']
            correo = request.form['correo_electronico']
            asunto = request.form['asunto']
            mensaje = request.form['mensaje']

            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO contacto (nombre_completo, correo_electronico, asunto, mensaje)
                VALUES (?, ?, ?, ?)
            """, (nombre, correo, asunto, mensaje))

            conexion.commit()
            conexion.close()

            return render_template('formu.html',
                                   nombre=nombre,
                                   correo=correo,
                                   asunto=asunto,
                                   mensaje=mensaje)

        except Exception as e:
            return f"Error en la base de datos: {e}"

    return render_template('formu.html')

# --- IMPORTANTE: no usar app.run() en PythonAnywhere ---
#if __name__ == "__main__":
#    app.run()  # <- comentar o quitar al subir a PythonAnywhere
