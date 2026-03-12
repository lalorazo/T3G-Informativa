from pymongo import MongoClient

print("🔍 Probando conexión directa a MongoDB...")

try:
    # Intentar conectar directamente
    client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=3000)
    
    # Verificar conexión
    client.admin.command('ping')
    print("✅ Conexión exitosa a MongoDB!")
    
    # Listar bases de datos
    dbs = client.list_database_names()
    print(f"📊 Bases de datos disponibles: {dbs}")
    
    # Usar nuestra base
    db = client['t3g_seguridad']
    
    # Ver colecciones
    collections = db.list_collection_names()
    print(f"📚 Colecciones en t3g_seguridad: {collections}")
    
    client.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Soluciones:")
    print("1. Asegúrate que MongoDB esté corriendo: net start MongoDB")
    print("2. Verifica que el puerto 27017 esté disponible")
    print("3. Si es necesario, reinstala MongoDB")