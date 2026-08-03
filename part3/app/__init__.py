from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app():
    """Application factory to configure and initialize the Flask app."""
    app = Flask(__name__)

    
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

   
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application Production API')

    # Register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app