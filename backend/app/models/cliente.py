from datetime import datetime
import bcrypt
from app.utils.database import mongo

class Cliente:
    collection = mongo.db.clientes
    
    @staticmethod
    def authenticate(codigo, email, password):
        """Autenticar cliente"""
        cliente = Cliente.collection.find_one({
            'email': email.lower(),
            'codigo_cliente': codigo.upper()
        })
        
        if not cliente:
            return None
        
        if not bcrypt.checkpw(password.encode('utf-8'), cliente['password']):
            return None
        
        # Actualizar último acceso
        Cliente.collection.update_one(
            {'_id': cliente['_id']},
            {'$set': {'ultimo_acceso': datetime.now()}}
        )
        
        return Cliente.to_dict(cliente)
    
    @staticmethod
    def get_by_id(cliente_id):
        """Obtener cliente por ID"""
        from bson.objectid import ObjectId
        cliente = Cliente.collection.find_one({'_id': ObjectId(cliente_id)})
        return Cliente.to_dict(cliente)
    
    @staticmethod
    def to_dict(cliente):
        """Convertir a diccionario sin datos sensibles"""
        if not cliente:
            return None
        
        cliente_dict = dict(cliente)
        cliente_dict.pop('password', None)
        cliente_dict['_id'] = str(cliente_dict['_id'])
        
        # Convertir fechas a string
        if 'fecha_registro' in cliente_dict:
            cliente_dict['fecha_registro'] = cliente_dict['fecha_registro'].isoformat()
        if 'ultimo_acceso' in cliente_dict and cliente_dict['ultimo_acceso']:
            cliente_dict['ultimo_acceso'] = cliente_dict['ultimo_acceso'].isoformat()
        
        return cliente_dict