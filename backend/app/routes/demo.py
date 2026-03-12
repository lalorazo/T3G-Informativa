from flask import Blueprint, request, jsonify
from app.models.solicitud_demo import SolicitudDemo
from app.config import Config
import urllib.parse

demo_bp = Blueprint('demo', __name__, url_prefix='/api/demo')

@demo_bp.route('/solicitar', methods=['POST'])
def solicitar():
    """Registrar solicitud de demo"""
    try:
        data = request.get_json()
        
        # Validar campos
        required = ['nombre', 'email', 'telefono', 'mensaje']
        for field in required:
            if field not in data or not data[field]:
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        # Guardar en MongoDB
        solicitud = SolicitudDemo.create(data)
        
        # Generar mailto para el frontend
        mailto = f"mailto:{Config.DEMO_EMAIL_DESTINO}"
        subject = urllib.parse.quote(f"Solicitud de Demo - {data['nombre']}")
        body = urllib.parse.quote(
            f"Nombre: {data['nombre']}\n"
            f"Email: {data['email']}\n"
            f"Teléfono: {data['telefono']}\n"
            f"Empresa: {data.get('empresa', 'No especificada')}\n"
            f"Kit de interés: {data.get('kit_interes', 'No especificado')}\n\n"
            f"Mensaje:\n{data['mensaje']}"
        )
        
        return jsonify({
            'success': True,
            'message': 'Solicitud recibida',
            'solicitud': solicitud,
            'mailto': f"{mailto}?subject={subject}&body={body}"
        }), 201
        
    except Exception as e:
        print(f"Error en demo: {e}")
        return jsonify({'error': 'Error del servidor'}), 500