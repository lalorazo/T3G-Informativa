from flask import Blueprint, request, jsonify
from app.utils.database import mongo
from datetime import datetime, timedelta
import jwt
from app.config import Config
import bcrypt
from bson import ObjectId

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login para clientes"""
    print("=" * 50)
    print("🔐 Login intentado")
    
    try:
        # Obtener datos del request
        data = request.get_json()
        print(f"📥 Datos recibidos: {data}")
        
        # Validar campos requeridos
        if not data:
            print("❌ No se recibieron datos")
            return jsonify({'error': 'No se recibieron datos', 'success': False}), 400
            
        codigo = data.get('codigo')
        email = data.get('email')
        password = data.get('password')
        
        print(f"📧 Email: {email}")
        print(f"🔑 Código: {codigo}")
        
        if not all([codigo, email, password]):
            print("❌ Faltan campos requeridos")
            return jsonify({'error': 'Todos los campos son requeridos', 'success': False}), 400
        
        # Conectar a MongoDB
        db = mongo.db
        if db is None:
            print("❌ MongoDB no está conectado")
            return jsonify({'error': 'Error de conexión a la base de datos', 'success': False}), 500
        
        # Buscar usuario por email
        print(f"🔍 Buscando usuario con email: {email}")
        usuario = db.clientes.find_one({'email': email.lower()})
        
        if not usuario:
            print(f"❌ Usuario no encontrado: {email}")
            return jsonify({'error': 'Credenciales inválidas', 'success': False}), 401
        
        print(f"✅ Usuario encontrado: {usuario.get('nombre')}")
        print(f"📋 Código en DB: {usuario.get('codigo_cliente')}")
        print(f"📋 Rol: {usuario.get('rol')}")
        
        # Verificar código
        if usuario.get('codigo_cliente') != codigo.upper():
            print(f"❌ Código incorrecto. Esperado: {usuario.get('codigo_cliente')}, Recibido: {codigo}")
            return jsonify({'error': 'Credenciales inválidas', 'success': False}), 401
        
        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), usuario['password']):
            print("❌ Contraseña incorrecta")
            return jsonify({'error': 'Credenciales inválidas', 'success': False}), 401
        
        print("✅ Contraseña correcta")
        
        # Actualizar último acceso
        db.clientes.update_one(
            {'_id': usuario['_id']},
            {'$set': {'ultimo_acceso': datetime.now()}}
        )
        
        # Generar token JWT
        token = jwt.encode({
            'cliente_id': str(usuario['_id']),
            'email': usuario['email'],
            'rol': usuario.get('rol', 'cliente'),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, Config.JWT_SECRET_KEY, algorithm='HS256')
        
        print(f"✅ Token generado para {usuario['email']}")
        
        # Preparar datos del usuario (sin contraseña)
        usuario_data = {
            '_id': str(usuario['_id']),
            'codigo_cliente': usuario.get('codigo_cliente'),
            'nombre': usuario.get('nombre'),
            'email': usuario.get('email'),
            'telefono': usuario.get('telefono'),
            'rol': usuario.get('rol', 'cliente'),
            'kit_adquirido': usuario.get('kit_adquirido'),
            'sensores_asignados': usuario.get('sensores_asignados', []),
            'direccion_instalacion': usuario.get('direccion_instalacion', {})
        }
        
        print("✅ Login exitoso")
        print("=" * 50)
        
        return jsonify({
            'success': True,
            'token': token,
            'cliente': usuario_data
        }), 200
        
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        return jsonify({'error': f'Error del servidor: {str(e)}', 'success': False}), 500