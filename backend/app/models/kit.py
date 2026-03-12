from app.utils.database import mongo

class Kit:
    collection = mongo.db.kits
    
    @staticmethod
    def get_all():
        """Obtener todos los kits activos"""
        kits = Kit.collection.find({'activo': True})
        return [Kit.to_dict(kit) for kit in kits]
    
    @staticmethod
    def get_by_tipo(tipo):
        """Obtener kit por tipo"""
        kit = Kit.collection.find_one({'tipo': tipo, 'activo': True})
        return Kit.to_dict(kit)
    
    @staticmethod
    def get_destacado():
        """Obtener kit destacado"""
        kit = Kit.collection.find_one({'destacado': True, 'activo': True})
        return Kit.to_dict(kit)
    
    @staticmethod
    def to_dict(kit):
        """Convertir ObjectId a string"""
        if not kit:
            return None
        kit['_id'] = str(kit['_id'])
        return kit