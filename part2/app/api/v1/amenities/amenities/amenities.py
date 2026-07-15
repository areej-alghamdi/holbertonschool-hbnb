from flask_restx import Namespace, Resource, fields
from app.services import facade

# Create the amenities namespace
api = Namespace('amenities', description='Amenity operations')

# Input model: used for POST and PUT requests
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Response model: what we send back to the client
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier of the amenity'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model, code=201)
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of amenities successfully retrieved')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """Retrieve all amenities"""
        return facade.get_all_amenities(), 200


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details successfully retrieved')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get a specific amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        """Update an existing amenity"""
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity, 200
        except ValueError as e:
            api.abort(400, str(e))
