from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Bad request')
    def post(self):
        """Register a new review"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        place_id = review_data.get('place_id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # التحقق من أن المستخدم لا يقيّم مكانه الخاص
        owner_id = place.owner.id if hasattr(place.owner, 'id') else place.owner
        if str(owner_id) == str(current_user_id):
            return {'error': 'You cannot review your own place'}, 400

        # التحقق من عدم التكرار
        all_reviews = facade.get_all_reviews()
        for r in all_reviews:
            r_user_id = r.user.id if hasattr(r.user, 'id') else r.user
            r_place_id = r.place.id if hasattr(r.place, 'id') else r.place
            if str(r_user_id) == str(current_user_id) and str(r_place_id) == str(place_id):
                return {'error': 'You have already reviewed this place'}, 400

        review_data['user_id'] = current_user_id
        new_review = facade.create_review(review_data)

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': current_user_id,
            'place_id': place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews (Public)"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (Public)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review (Only creator can modify)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        r_user_id = review.user.id if hasattr(review.user, 'id') else review.user
        if str(r_user_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        review_data = api.payload
        facade.update_review(review_id, review_data)
        return {'message': 'Review updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review (Only creator can delete)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        r_user_id = review.user.id if hasattr(review.user, 'id') else review.user
        if str(r_user_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200