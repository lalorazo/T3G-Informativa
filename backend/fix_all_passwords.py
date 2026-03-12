from pymongo import MongoClient
import bcrypt
from datetime import datetime

print("=" * 60)
print("🔧 CORRECTOR DE CONTRASEÑAS T3G")
print("=" * 60)

try:
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['t3g_seguridad']
    
    print("📡 Conectado a MongoDB")
    
    # 1. Ver todas las contraseñas actuales
    print("\n📋 Verificando estado actual:")
    usuarios = db.clientes.find()
    for user in usuarios:
        print(f"   - {user.get('email')}: Tipo de password: {type(user.get('password'))}")
    
    # 2. CORREGIR: Lista de usuarios con sus contraseñas en texto plano
    usuarios_corregir = [
        {"email": "admin@t3g.com", "password": "admin123", "nombre": "Administrador"},
        {"email": "juan@email.com", "password": "cliente123", "nombre": "Juan Pérez"},
        {"email": "maria@email.com", "password": "cliente123", "nombre": "María García"},
    ]
    
    print("\n🔄 Corrigiendo contraseñas...")
    
    for usuario in usuarios_corregir:
        # Generar hash en formato binario (bytes)
        password_bytes = usuario["password"].encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)
        
        # Actualizar en MongoDB
        resultado = db.clientes.update_one(
            {"email": usuario["email"]},
            {
                "$set": {
                    "password": password_hash,
                    "activo": True,
                    "ultimo_acceso": None
                }
            }
        )
        
        if resultado.matched_count > 0:
            print(f"   ✅ {usuario['nombre']}: contraseña corregida")
            
            # Verificar que funciona
            verificado = bcrypt.checkpw(password_bytes, password_hash)
            print(f"      Verificación: {'✅ OK' if verificado else '❌ FALLO'}")
        else:
            print(f"   ❌ {usuario['email']}: no encontrado, creando...")
            
            # Si no existe, crearlo
            nuevo_usuario = {
                "codigo_cliente": f"T3G-{usuario['email'].split('@')[0].upper()}",
                "nombre": usuario["nombre"],
                "email": usuario["email"],
                "password": password_hash,
                "telefono": "5512345678",
                "activo": True,
                "fecha_registro": datetime.now(),
                "rol": "admin" if usuario["email"] == "admin@t3g.com" else "cliente",
                "kit_adquirido": None if usuario["email"] == "admin@t3g.com" else "profesional",
                "sensores_asignados": [] if usuario["email"] == "admin@t3g.com" else [
                    {"tipo": "camara", "identificador": "CAM-001", "ubicacion": "Entrada"}
                ]
            }
            db.clientes.insert_one(nuevo_usuario)
            print(f"      ✅ Usuario creado")
    
    # 3. Verificación final
    print("\n🔍 Verificación final:")
    for usuario in usuarios_corregir:
        user = db.clientes.find_one({"email": usuario["email"]})
        if user:
            try:
                verificado = bcrypt.checkpw(usuario["password"].encode('utf-8'), user["password"])
                print(f"   - {usuario['email']}: {'✅ OK' if verificado else '❌ FALLO'}")
            except Exception as e:
                print(f"   - {usuario['email']}: ❌ Error - {e}")
        else:
            print(f"   - {usuario['email']}: ❌ No encontrado")
    
    # 4. Mostrar resumen de credenciales
    print("\n" + "=" * 60)
    print("📝 CREDENCIALES ACTUALIZADAS:")
    print("=" * 60)
    print("   ADMIN:")
    print("   - Email: admin@t3g.com")
    print("   - Password: admin123")
    print("   - Código: T3G-ADMIN-001")
    print()
    print("   CLIENTES:")
    print("   - Email: juan@email.com")
    print("   - Password: cliente123")
    print("   - Código: T3G-001")
    print()
    print("   - Email: maria@email.com")
    print("   - Password: cliente123")
    print("   - Código: T3G-002")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()