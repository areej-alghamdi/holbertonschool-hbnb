from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# 1. نموذج الإدخال عند إنشاء مستخدم جديد (يتضمن كلمة المرور)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# 2. نموذج الإرجاع (استبعاد كلمة المرور نهائياً)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Email already registered or invalid input')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # التأكد من عدم تكرار البريد الإلكتروني
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)

        # إرجاع بيانات المستخدم بدون كلمة المرور
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.marshal_list_with(user_response_model)
    def get(self):
        """Get list of all users without exposing passwords"""
        users = facade.get_all_users()
        return users

@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID without exposing password"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user