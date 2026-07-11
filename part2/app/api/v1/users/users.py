from flask import request
from flask_restx import Namespace, Resource, fields
# Import the actual instance of HBnBFacade
from app.services import facade

api = Namespace('users', description='User operations')

# Define the expected JSON structure for user creation validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already exists or invalid input')
    def post(self):
        """Register a new user inside the system."""
        user_data = api.payload
        try:
            # Pass the data to the facade for business logic and validation
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            # Handle validation errors or duplicate email exceptions
            return {'error': str(e)}, 400
