from flask import Flask
from flask_restx import Api

def create_app():
    """Application factory to configure and initialize the Flask app."""
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application Production API')

    # Register namespaces
    from app.api.v1.users.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    return app
