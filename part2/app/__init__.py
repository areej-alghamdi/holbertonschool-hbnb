from flask import Flask
from flask_restx import Api
 
 
def create_app():
    """Application factory to configure and initialize the Flask app."""
    app = Flask(__name__)
 
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application Production API')
 
    # Register namespaces
    from app.api.v1.users.users import api as users_ns
    from app.api.v1.amenities.amenities import api as amenities_ns
    from app.api.v1.places.places import api as places_ns
 
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
 
    return app