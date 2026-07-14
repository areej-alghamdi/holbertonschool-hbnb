
Places · PY
from flask_restx import Namespace, Resource, fields
from app.services import facade
 
# Create the places namespace
api = Namespace('places', description='Place operations')
 
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
 
 
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Create a new place"""
        place_data = api.payload
 
        # Check that the owner exists
        owner = facade.get_user(place_data.get('owner_id'))
        if not owner:
            return {'error': 'Owner not found'}, 404
 
        # Validate amenity IDs if provided
        amenity_ids = place_data.get('amenity_ids', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': f'Amenity {amenity_id} not found'}, 404
            amenities.append(amenity)
 
        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                },
                'amenities': [
                    {'id': a.id, 'name': a.name} for a in amenities
                ],
                'created_at': str(new_place.created_at),
                'updated_at': str(new_place.updated_at)
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
 
    @api.response(200, 'List of places successfully retrieved')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        result = []
        for place in places:
            result.append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'created_at': str(place.created_at),
                'updated_at': str(place.updated_at)
            })
        return result, 200
 
 
@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.response(200, 'Place details successfully retrieved')
    def get(self, place_id):
        """Get a specific place by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
 
        # Get owner details
        owner = facade.get_user(place.owner_id)
 
        # Get amenity details
        amenities = []
        for amenity_id in place.amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities.append({'id': amenity.id, 'name': amenity.name})
 
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } if owner else None,
            'amenities': amenities,
            'created_at': str(place.created_at),
            'updated_at': str(place.updated_at)
        }, 200
 
    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input data')
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
                return {'error': f'Amenity {amenity_id} not found'}, 404
 
        try:
            updated_place = facade.update_place(place_id, place_data)
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'created_at': str(updated_place.created_at),
                'updated_at': str(updated_place.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
 








