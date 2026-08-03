from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


# 1. إنشاء كائنات التشفير والـ JWT
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    """Application factory to configure and initialize the Flask app."""
    app = Flask(__name__)

    # 2. إعداد المفتاح السري للـ JWT (ضروري للتشفير والتوكنات)
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    # 3. ربط الملحقات بالتطبيق
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application Production API')

    # Register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    ##sql
    db = SQLAlchemy()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    return app
