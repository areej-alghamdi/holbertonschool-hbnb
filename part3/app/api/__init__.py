from flask import Flask
from flask_jwt_extended import JWTManager
from app.api.v1 import blueprint as api_v1_blueprint

def create_app():
    app = Flask(__name__)
    
    # مفتاح الأمان للـ JWT
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    
    # تهيئة الـ JWT
    jwt = JWTManager(app)
    
    # تسجيل الـ API Blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
    
    return app