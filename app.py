from flask import Flask, render_template, request, jsonify, send_from_directory
from database import Database
import re
import concurrent.futures
import random
import threading
import traceback
from flask_cors import CORS
import socket
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

db = Database()
db_lock = threading.Lock()

def get_local_ip():
    """Obtiene la IP local de la máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Ruta principal - SERVIR INDEX.HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta explícita para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Ruta para servir CSS
@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

# Ruta para servir JS
@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

# API Routes
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        usuarios = db.obtener_usuarios()
        print(f"Obtenidos {len(usuarios)} usuarios de la BD")
        return jsonify(usuarios)
    except Exception as e:
        error_msg = f"Error obteniendo usuarios: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        edad = data.get('edad')
        
        print(f"Recibiendo datos: nombre={nombre}, apellido={apellido}, edad={edad}")
        
        if not nombre or not apellido or not edad:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400
        
        usuario_id = db.agregar_usuario(nombre, apellido, edad)
        if usuario_id:
            return jsonify({
                'id': usuario_id, 
                'mensaje': 'Usuario agregado correctamente',
                'usuario': {'id': usuario_id, 'nombre': nombre, 'apellido': apellido, 'edad': edad}
            })
        else:
            return jsonify({'error': 'Error al agregar usuario a la base de datos'}), 500
    except Exception as e:
        error_msg = f"Error agregando usuario: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/usuarios/aleatorios', methods=['POST'])
def generar_usuarios_aleatorios():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        cantidad = data.get('cantidad', 1000)
        
        print(f"Solicitando generar {cantidad} usuarios aleatorios...")
        
        usuarios_generados = generar_usuarios_masivos(cantidad)
        
        response_data = {
            'mensaje': f'Se generaron {len(usuarios_generados)} usuarios aleatorios',
            'usuarios': usuarios_generados
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        error_msg = f"Error generando usuarios aleatorios: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    try:
        print(f"Eliminando usuario con ID: {usuario_id}")
        db.eliminar_usuario(usuario_id)
        return jsonify({'mensaje': 'Usuario eliminado correctamente'})
    except Exception as e:
        error_msg = f"Error eliminando usuario: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/usuarios/todos', methods=['DELETE'])
def eliminar_todos_usuarios():
    try:
        print("Eliminando todos los usuarios...")
        db.eliminar_todos_usuarios()
        return jsonify({'mensaje': 'Todos los usuarios han sido eliminados'})
    except Exception as e:
        error_msg = f"Error eliminando todos los usuarios: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/generar-correos', methods=['POST'])
def generar_correos():
    try:
        print("🚀 Iniciando generación MASIVA de correos...")
        start_time = datetime.now()
        
        usuarios = db.obtener_usuarios()
        
        if not usuarios:
            return jsonify({'error': 'No hay usuarios para generar correos'}), 400
        
        print(f"📧 Generando correos para {len(usuarios)} usuarios...")
        
        # OPTIMIZACIÓN: Usar inserción por lotes
        correos_generados = generar_correos_masivos(usuarios)
        
        end_time = datetime.now()
        tiempo_total = (end_time - start_time).total_seconds()
        
        print(f"✅ Generados {len(correos_generados)} correos en {tiempo_total:.2f} segundos")
        
        return jsonify({
            'mensaje': f'Se generaron {len(correos_generados)} correos electrónicos en {tiempo_total:.2f} segundos',
            'correos': correos_generados,
            'tiempo': tiempo_total
        })
    
    except Exception as e:
        error_msg = f"Error generando correos: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/correos', methods=['GET'])
def obtener_correos():
    try:
        correos = db.obtener_correos()
        print(f"Obtenidos {len(correos)} correos de la BD")
        return jsonify(correos)
    except Exception as e:
        error_msg = f"Error obteniendo correos: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/correos/todos', methods=['DELETE'])
def eliminar_todos_correos():
    try:
        print("Eliminando todos los correos...")
        db.eliminar_todos_correos()
        return jsonify({'mensaje': 'Todos los correos han sido eliminados'})
    except Exception as e:
        error_msg = f"Error eliminando todos los correos: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

# Manejo de errores para rutas no encontradas
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

# Funciones auxiliares
def generar_usuarios_masivos(cantidad):
    """Genera usuarios aleatorios de forma masiva"""
    nombres = [
        'Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sofía', 
        'José', 'Elena', 'Miguel', 'Isabel', 'David', 'Carmen', 'Javier', 'Rosa',
        'Daniel', 'Patricia', 'Francisco', 'Lucía', 'Antonio', 'Teresa', 'Manuel', 'Eva',
        'Jorge', 'Marta', 'Pablo', 'Cristina', 'Alberto', 'Silvia', 'Fernando', 'Raquel'
    ]
    
    apellidos = [
        'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez',
        'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Ruiz', 'Hernández', 'Díaz', 'Moreno',
        'Álvarez', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro', 'Torres', 'Domínguez',
        'Vázquez', 'Ramos', 'Gil', 'Ramírez', 'Serrano', 'Blanco', 'Molina', 'Morales'
    ]
    
    usuarios_generados = []
    
    for i in range(cantidad):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        edad = random.randint(18, 80)
        
        usuario_id = db.agregar_usuario(nombre, apellido, edad)
        
        if usuario_id:
            usuarios_generados.append({
                'id': usuario_id,
                'nombre': nombre,
                'apellido': apellido,
                'edad': edad
            })
    
    return usuarios_generados

def generar_correos_masivos(usuarios):
    """Genera correos para todos los usuarios usando inserción por lotes"""
    todos_los_correos = []
    
    for usuario in usuarios:
        correos_generados = generar_correos_usuario(usuario['nombre'], usuario['apellido'])
        for tipo, correo in correos_generados.items():
            todos_los_correos.append({
                'usuario_id': usuario['id'],
                'tipo': tipo,
                'correo': correo
            })
    
    # Insertar en un solo lote masivo
    if todos_los_correos:
        print(f"💾 Insertando {len(todos_los_correos)} correos en lote único...")
        db.guardar_correos_lote(todos_los_correos)
    
    return todos_los_correos

def generar_correos_usuario(nombre, apellido):
    """Genera diferentes formatos de correo para un usuario"""
    try:
        # Normalizar nombres
        regex_limpiar = re.compile(r'[^a-zA-Z]')
        nombre_limpio = regex_limpiar.sub('', nombre).lower()
        apellido_limpio = regex_limpiar.sub('', apellido).lower()
        
        # Pre-calcular valores
        inicial_nombre = nombre_limpio[0] if nombre_limpio else 'a'
        inicial_apellido = apellido_limpio[0] if apellido_limpio else 'b'
        
        # Generar diferentes formatos de correo
        correos = {
            'gmail': f"{nombre_limpio}.{apellido_limpio}@gmail.com",
            'outlook': f"{nombre_limpio}_{apellido_limpio}@outlook.com",
            'hotmail': f"{inicial_nombre}{apellido_limpio}@hotmail.com",
            'yahoo': f"{nombre_limpio}-{apellido_limpio}@yahoo.com",
            'empresa': f"{inicial_nombre}.{apellido_limpio}@empresa.com",
            'custom1': f"{nombre_limpio}{apellido_limpio}@custom.com",
            'custom2': f"{apellido_limpio}.{nombre_limpio}@company.com",
            'custom3': f"{inicial_nombre}{inicial_apellido}@corporate.com"
        }
        
        return correos
    except Exception as e:
        print(f"Error generando correos usuario: {str(e)}")
        return {}

if __name__ == '__main__':
    # Crear tablas si no existen
    try:
        print("Verificando/Creando tablas en la base de datos...")
        db.crear_tablas()
        print("Tablas verificadas/creadas correctamente")
    except Exception as e:
        print(f"Error creando tablas: {e}")
    
    # Configuración de red
    local_ip = get_local_ip()
    port = 5000
    
    print("\n" + "="*60)
    print("SERVIDOR CRM - ACCESO POR RED HABILITADO")
    print("="*60)
    print(f" Acceso local:    http://localhost:{port}")
    print(f" Acceso en red:   http://{local_ip}:{port}")
    print("="*60)
    print(" Rutas disponibles:")
    print("   • /              -> Interfaz web")
    print("   • /static/*      -> Archivos CSS/JS")
    print("   • /usuarios      -> API Usuarios")
    print("   • /correos       -> API Correos")
    print("="*60)
    print("Para que otros se conecten:")
    print(f" Usen en sus navegadores: http://{local_ip}:{port}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)