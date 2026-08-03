from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.admin import admin_required
from flask import request

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])

        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'You cannot modify email or password')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Modify user details.

        Regular users: can edit their own profile, but NOT email/password.
        Admins: can edit any user, including email/password.
        """
        current_user_id = get_jwt_identity()

        # تحقق هل المستخدم أدمن
        is_admin = facade.get_user(current_user_id).is_admin if facade.get_user(current_user_id) else False

        if not is_admin:
            if str(user_id) != str(current_user_id):
                return {'error': 'Unauthorized action'}, 403

            user_data = api.payload
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
        else:
            user_data = request.json
            email = user_data.get('email')
            if email:
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email is already in use'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        updated_user = facade.update_user(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'is_admin': updated_user.is_admin
        }, 200