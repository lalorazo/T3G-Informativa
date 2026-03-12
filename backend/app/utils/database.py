from flask_pymongo import PyMongo
from pymongo import ASCENDING, DESCENDING
import bcrypt
from datetime import datetime

mongo = PyMongo()

def init_db(app):
    """Inicializar conexión a MongoDB y crear datos por defecto"""
    
    print(f"📡 Conectando a MongoDB: {app.config.get('MONGODB_URI')}")
    
    try:
        # Configurar PyMongo
        app.config['MONGO_URI'] = app.config.get('MONGODB_URI')
        mongo.init_app(app)
        
        with app.app_context():
            db = mongo.db
            
            # Verificar conexión
            db.command('ping')
            print("✅ Conexión a MongoDB exitosa")
            
            # Crear colección kits si no existe
            if 'kits' not in db.list_collection_names():
                db.create_collection('kits')
                print("✅ Colección 'kits' creada")
            
            # Insertar kits si no existen
            if db.kits.count_documents({}) == 0:
                print("📦 Insertando kits iniciales...")
                kits_iniciales = [
                    {
                        'nombre': 'Kit Residencial',
                        'tipo': 'residencial',
                        'precio': 12999.00,
                        'descripcion': 'Ideal para hogares',
                        'sensores': {
                            'camaras': 2,
                            'gas': 1,
                            'movimiento': 1,
                            'calor': 0
                        },
                        'incluye_instalacion': True,
                        'meses_monitoreo_gratis': 3,
                        'activo': True,
                        'destacado': False
                    },
                    {
                        'nombre': 'Kit Profesional',
                        'tipo': 'profesional',
                        'precio': 24452.48,
                        'descripcion': '4 cámaras + sensores completos',
                        'sensores': {
                            'camaras': 4,
                            'gas': 2,
                            'movimiento': 2,
                            'calor': 2
                        },
                        'incluye_instalacion': True,
                        'meses_monitoreo_gratis': 12,
                        'activo': True,
                        'destacado': True
                    },
                    {
                        'nombre': 'Kit Empresarial',
                        'tipo': 'empresarial',
                        'precio': 45999.00,
                        'descripcion': 'Sistema completo para negocios',
                        'sensores': {
                            'camaras': 8,
                            'gas': 4,
                            'movimiento': 4,
                            'calor': 4
                        },
                        'incluye_instalacion': True,
                        'meses_monitoreo_gratis': 24,
                        'activo': True,
                        'destacado': False
                    }
                ]
                
                resultado = db.kits.insert_many(kits_iniciales)
                print(f"✅ {len(resultado.inserted_ids)} kits insertados")
            else:
                print(f"✅ Los kits ya existen ({db.kits.count_documents({})} kits)")
            
            # Crear admin si no existe
            if db.clientes.count_documents({'email': 'admin@t3g.com'}) == 0:
                print("👤 Creando usuario administrador...")
                password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
                
                admin = {
                    'codigo_cliente': 'T3G-ADMIN-001',
                    'nombre': 'Administrador',
                    'email': 'admin@t3g.com',
                    'password': password_hash,
                    'telefono': '5512345678',
                    'activo': True,
                    'fecha_registro': datetime.now(),
                    'rol': 'admin',
                    'kit_adquirido': None
                }
                
                db.clientes.insert_one(admin)
                print("✅ Admin creado")
            
            print("\n📊 Resumen:")
            print(f"   - Clientes: {db.clientes.count_documents({})}")
            print(f"   - Kits: {db.kits.count_documents({})}")
            
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        print("📌 Verifica que:")
        print("   1. MongoDB esté corriendo (net start MongoDB)")
        print("   2. La URI sea correcta: mongodb://localhost:27017")
        print("   3. El puerto 27017 no esté bloqueado")