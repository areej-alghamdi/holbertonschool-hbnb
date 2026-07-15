from flask_restx import Namespace, Resource, fields
from app.services import facade

# Create the places namespace
api = Namespace('places', description='Place operations')

# Related Models for nested response representation
place_owner_model = api.model('PlaceOwner', {
    'id': fields.String(description='ID of the owner'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='ID of the amenity'),
    'name': fields.String(description='Name of the amenity')
})

# Input model: used for POST requests
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})

# Update model: used for PUT requests (all fields optional)
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})

# Response model for detailed Place representation (includes Nested fields)
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Unique identifier of the place'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(place_owner_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(place_amenity_model), description='List of amenities'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

# Response model for listing Places (simplified)
place_list_response_model = api.model('PlaceListResponse', {
    'id': fields.String(description='Unique identifier of the place'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner or Amenity not found')
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        """Create a new place"""
        place_data = api.payload

        # Check that the owner exists
        owner = facade.get_user(place_data.get('owner_id'))
        if not owner:
            api.abort(404, 'Owner not found')

        # Validate amenity IDs if provided
        amenity_ids = place_data.get('amenity_ids', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, f'Amenity {amenity_id} not found')
            amenities.append(amenity)

        try:
            new_place = facade.create_place(place_data)
            # Match the response data to the place_response_model expectations
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner': owner,
                'amenities': amenities,
                'created_at': str(new_place.created_at),
                'updated_at': str(new_place.updated_at)
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places successfully retrieved')
    @api.marshal_list_with(place_list_response_model)
    def get(self):
        """Retrieve all places"""
        return facade.get_all_places(), 200


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.response(200, 'Place details successfully retrieved')
    @api.marshal_with(place_response_model)
    def get(self, place_id):
        """Get a specific place by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        # Get owner details
        owner = facade.get_user(place.owner_id)

        # Get amenity details
        amenities = []
        for amenity_id in getattr(place, 'amenity_ids', []):
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities.append(amenity)

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner,
            'amenities': amenities,
            'created_at': str(place.created_at),
            'updated_at': str(place.updated_at)
        }, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(place_list_response_model)
    def put(self, place_id):
        """Update an existing place"""
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        # Validate amenity IDs if provided
        amenity_ids = place_data.get('amenity_ids', [])
        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, f'Amenity {amenity_id} not found')

        try:
            updated_place = facade.update_place(place_id, place_data)
            return updated_place, 200
        except ValueError as e:
            api.abort(400, str(e))
