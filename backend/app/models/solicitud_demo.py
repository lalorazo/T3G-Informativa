from datetime import datetime
from app.utils.database import mongo

class SolicitudDemo:
    collection = mongo.db.solicitudes_demo
    
    @staticmethod
    def create(data):
        """Crear nueva solicitud"""
        solicitud = {
            'nombre': data['nombre'],
            'email': data['email'].lower(),
            'telefono': data['telefono'],
            'empresa': data.get('empresa', ''),
            'mensaje': data['mensaje'],
            'fecha_solicitud': datetime.now(),
            'estado': 'pendiente',
            'kit_interes': data.get('kit_interes', ''),
            'link_enviado': None,
            'fecha_envio': None
        }
        
        result = SolicitudDemo.collection.insert_one(solicitud)
        solicitud['_id'] = str(result.inserted_id)
        return solicitud
    
    @staticmethod
    def get_all():
        """Obtener todas las solicitudes"""
        solicitudes = SolicitudDemo.collection.find().sort('fecha_solicitud', -1)
        return [SolicitudDemo.to_dict(s) for s in solicitudes]
    
    @staticmethod
    def to_dict(solicitud):
        """Convertir ObjectId a string"""
        if not solicitud:
            return None
        solicitud['_id'] = str(solicitud['_id'])
        solicitud['fecha_solicitud'] = solicitud['fecha_solicitud'].isoformat()
        return solicitud