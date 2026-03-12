from pymongo import MongoClient

print("🔄 Conectando a MongoDB...")

try:
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['t3g_seguridad']
    
    # Verificar si ya hay kits
    kits_count = db.kits.count_documents({})
    print(f"📊 Kits existentes: {kits_count}")
    
    if kits_count == 0:
        print("📦 Insertando kits...")
        
        kits = [
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
        
        resultado = db.kits.insert_many(kits)
        print(f"✅ {len(resultado.inserted_ids)} kits insertados correctamente")
        
    else:
        print("✅ Los kits ya existen en la base de datos")
    
    # Mostrar los kits insertados
    print("\n📋 Kits en la base de datos:")
    for kit in db.kits.find():
        print(f"   - {kit['nombre']}: ${kit['precio']} MXN")
        
except Exception as e:
    print(f"❌ Error: {e}")