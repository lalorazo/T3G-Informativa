from flask import Blueprint, jsonify, request
from app.utils.database import mongo
from bson import ObjectId
import jwt
from app.config import Config
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Middleware para verificar token de admin
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            # Verificar que sea admin
            db = mongo.db
            admin = db.clientes.find_one({'_id': ObjectId(payload['cliente_id'])})
            
            if not admin or admin.get('rol') != 'admin':
                return jsonify({'error': 'Acceso no autorizado'}), 403
                
            kwargs['admin_id'] = payload['cliente_id']
            return f(*args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    
    return decorated

@admin_bp.route('/clientes', methods=['GET'])
@token_required
def get_clientes(admin_id):
    """Obtener todos los clientes (solo admin)"""
    try:
        db = mongo.db
        clientes = list(db.clientes.find())
        
        # Convertir ObjectId a string y remover contraseñas
        for cliente in clientes:
            cliente['_id'] = str(cliente['_id'])
            if 'password' in cliente:
                del cliente['password']
            if 'fecha_registro' in cliente:
                cliente['fecha_registro'] = cliente['fecha_registro'].isoformat() if cliente['fecha_registro'] else None
        
        return jsonify(clientes), 200
        
    except Exception as e:
        print(f"Error obteniendo clientes: {e}")
        return jsonify({'error': 'Error del servidor'}), 500

@admin_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(admin_id):
    """Obtener estadísticas generales"""
    try:
        db = mongo.db
        
        # Total clientes
        total_clientes = db.clientes.count_documents({})
        
        # Total kits
        total_kits = db.kits.count_documents({})
        
        # Total cámaras (sumar de todos los kits)
        kits = list(db.kits.find())
        total_camaras = sum(kit.get('sensores', {}).get('camaras', 0) for kit in kits)
        
        # Solicitudes demo pendientes
        solicitudes_pendientes = db.solicitudes_demo.count_documents({'estado': 'pendiente'})
        
        return jsonify({
            'total_clientes': total_clientes,
            'total_kits': total_kits,
            'total_camaras': total_camaras,
            'solicitudes_pendientes': solicitudes_pendientes
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo stats: {e}")
        return jsonify({'error': 'Error del servidor'}), 500

@admin_bp.route('/kits', methods=['GET'])
@token_required
def get_kits_admin(admin_id):
    """Obtener todos los kits (para admin)"""
    try:
        db = mongo.db
        kits = list(db.kits.find())
        
        for kit in kits:
            kit['_id'] = str(kit['_id'])
        
        return jsonify(kits), 200
        
    except Exception as e:
        print(f"Error obteniendo kits: {e}")
        return jsonify({'error': 'Error del servidor'}), 500

@admin_bp.route('/demos', methods=['GET'])
@token_required
def get_demos(admin_id):
    """Obtener todas las solicitudes de demo"""
    try:
        db = mongo.db
        demos = list(db.solicitudes_demo.find().sort('fecha_solicitud', -1))
        
        for demo in demos:
            demo['_id'] = str(demo['_id'])
            if 'fecha_solicitud' in demo:
                demo['fecha_solicitud'] = demo['fecha_solicitud'].isoformat() if demo['fecha_solicitud'] else None
        
        return jsonify(demos), 200
        
    except Exception as e:
        print(f"Error obteniendo demos: {e}")
        return jsonify({'error': 'Error del servidor'}), 500