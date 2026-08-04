from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services import facade
from app.api.v1.admin import admin_required


api = Namespace("users", description="User operations")


user_model = api.model("User", {
    "first_name": fields.String(
        required=True,
        description="First name of the user"
    ),
    "last_name": fields.String(
        required=True,
        description="Last name of the user"
    ),
    "email": fields.String(
        required=True,
        description="Email of the user"
    ),
    "password": fields.String(
        required=True,
        description="Password of the user"
    ),
    "is_admin": fields.Boolean(
        required=False,
        description="Administrative status"
    )
})


user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(
        required=False,
        description="First name of the user"
    ),
    "last_name": fields.String(
        required=False,
        description="Last name of the user"
    ),
    "email": fields.String(
        required=False,
        description="Email of the user"
    ),
    "password": fields.String(
        required=False,
        description="Password of the user"
    ),
    "is_admin": fields.Boolean(
        required=False,
        description="Administrative status"
    )
})


@api.route("/")
class UserList(Resource):
    @jwt_required()
    @admin_required()
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered or invalid input data")
    @api.response(403, "Admin privileges required")
    def post(self):
        """Create a new user as an administrator."""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)

            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "is_admin": new_user.is_admin
            }, 201

        except ValueError as error:
            return {"error": str(error)}, 400

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Retrieve a list of all users."""
        users = facade.get_all_users()

        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_admin": user.is_admin
            }
            for user in users
        ], 200


@api.route("/<string:user_id>")
@api.param("user_id", "The user identifier")
class UserResource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID."""
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }, 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, "User details updated successfully")
    @api.response(400, "Invalid update data")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update a user profile.

        Regular users may update only their own first and last names.
        Administrators may update any user, including email and password.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        user_data = api.payload

        if not is_admin:
            if str(user_id) != str(current_user_id):
                return {"error": "Unauthorized action"}, 403

            if (
                "email" in user_data
                or "password" in user_data
                or "is_admin" in user_data
            ):
                return {
                    "error": "You cannot modify email or password"
                }, 400

        try:
            updated_user = facade.update_user(user_id, user_data)

            return {
                "id": updated_user.id,
                "first_name": updated_user.first_name,
                "last_name": updated_user.last_name,
                "email": updated_user.email,
                "is_admin": updated_user.is_admin
            }, 200

        except ValueError as error:
            return {"error": str(error)}, 400
