from flask import Blueprint, jsonify
from app.models.kit import Kit

kits_bp = Blueprint('kits', __name__, url_prefix='/api/kits')

@kits_bp.route('/', methods=['GET'])
def get_kits():
    """Obtener todos los kits"""
    try:
        kits = Kit.get_all()
        return jsonify(kits), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error del servidor'}), 500

@kits_bp.route('/destacado', methods=['GET'])
def get_destacado():
    """Obtener kit destacado"""
    try:
        kit = Kit.get_destacado()
        return jsonify(kit), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error del servidor'}), 500

@kits_bp.route('/<tipo>', methods=['GET'])
def get_kit(tipo):
    """Obtener kit por tipo"""
    try:
        kit = Kit.get_by_tipo(tipo)
        if not kit:
            return jsonify({'error': 'Kit no encontrado'}), 404
        return jsonify(kit), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error del servidor'}), 500