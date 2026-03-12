from pymongo import MongoClient
from datetime import datetime

print("🔍 Verificando datos en MongoDB...")

try:
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['t3g_seguridad']
    
    # Ver colecciones
    print("\n📚 Colecciones encontradas:")
    collections = db.list_collection_names()
    for col in collections:
        count = db[col].count_documents({})
        print(f"   - {col}: {count} documentos")
    
    # Ver kits
    print("\n📦 Kits disponibles:")
    kits = db.kits.find()
    for kit in kits:
        print(f"   - {kit['nombre']}: ${kit['precio']} MXN")
    
    # Ver clientes
    print("\n👤 Clientes registrados:")
    clientes = db.clientes.find()
    for cliente in clientes:
        print(f"   - {cliente.get('nombre', 'N/A')}: {cliente.get('email', 'N/A')}")
    
except Exception as e:
    print(f"❌ Error: {e}")