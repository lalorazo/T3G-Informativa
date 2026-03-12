from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.utils.database import init_db, mongo
from app.routes.admin import admin_bp
import os

def create_app():
    app = Flask(__name__)
    
    # FORZAR configuración de MongoDB directamente
    app.config['MONGODB_URI'] = 'mongodb://localhost:27017/t3g_seguridad'
    app.config['MONGODB_DB'] = 't3g_seguridad'
    app.config['SECRET_KEY'] = 'dev-key-123'
    app.config['JWT_SECRET_KEY'] = 'jwt-key-456'
    
    print("🔧 Configuración forzada:")
    print(f"   MONGODB_URI: {app.config['MONGODB_URI']}")
    print(f"   MONGODB_DB: {app.config['MONGODB_DB']}")
    
    # Habilitar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5500", "http://127.0.0.1:5500"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Inicializar MongoDB
    print("📡 Inicializando MongoDB...")
    init_db(app)
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.kits import kits_bp
    from app.routes.demo import demo_bp
    from app.routes.admin import admin_bp  

    app.register_blueprint(auth_bp)
    app.register_blueprint(kits_bp)
    app.register_blueprint(demo_bp)
    app.register_blueprint(admin_bp)

    # Ruta de prueba
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'mongodb': 'connected' if mongo.db else 'disconnected',
            'message': 'Servidor T3G funcionando'
        })
    
    return app