from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# 1. Input Model: Includes password for registration (POST)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password for the user account')
})

# 2. Update Model: Used for PUT requests (Omits password entirely)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address of the user')
})

# 3. Response Model: STOPS password from being returned to the client (Security best practice)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='Unique identifier of the user'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address of the user'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already exists or invalid input')
    @api.marshal_with(user_response_model, code=201)  # Uses response model (No password returned)
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
            return new_user, 201
        except ValueError as e:
            # استخدام api.abort يضمن خروج رسالة الخطأ وتخطي الـ marshal_with
            api.abort(400, str(e))

    @api.response(200, 'List of users successfully retrieved')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """Retrieve a list of all users"""
        return facade.get_all_users(), 200


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.response(200, 'User details successfully retrieved')
    @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.expect(user_update_model, validate=True)  # Validates fields based on update model
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Email already exists or invalid input')
    @api.marshal_with(user_response_model)
    def put(self, user_id):
        """Update user details (Password modification is not allowed here)"""
        user_data = api.payload.copy()
        
        # 2.3 PUT: Prevent updating the password right now. Keep it as it is.
        if 'password' in user_data:
            del user_data['password']
            
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
            
        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user, 200
        except ValueError as e:
            api.abort(400, str(e))
