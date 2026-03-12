from app import create_app
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = create_app()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Servidor T3G funcionando!")
    print("📡 API: http://localhost:5000")
    print("📊 MongoDB: Conectado")
    print("="*50 + "\n")
    
    # usar=False evita el doble reload
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)