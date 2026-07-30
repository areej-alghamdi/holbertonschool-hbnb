from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False),
    'rating': fields.Integer(required=False)
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        data = api.payload or {}
        text = data.get('text')
        rating = data.get('rating')
        user_id = data.get('user_id')
        place_id = data.get('place_id')

        if not text or not str(text).strip():
            return {'error': 'Text is required and cannot be empty'}, 400

        if rating is None or not isinstance(rating, int) or isinstance(rating, bool) or not (1 <= rating <= 5):
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        if not user_id:
            return {'error': 'user_id is required'}, 400

        if not place_id:
            return {'error': 'place_id is required'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        try:
            review = facade.create_review(data)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': user.id,
                'place_id': place.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Success')
    def get(self):
        reviews = facade.get_all_reviews()
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user.id if hasattr(r.user, 'id') else r.user_id,
            'place_id': r.place.id if hasattr(r.place, 'id') else r.place_id
        } for r in reviews], 200


@api.route('/<review_id>')
@api.param('review_id', 'The Review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id if hasattr(review.user, 'id') else review.user_id,
            'place_id': review.place.id if hasattr(review.place, 'id') else review.place_id
        }, 200

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        data = api.payload or {}

        if 'text' in data:
            text = data['text']
            if text is None or not str(text).strip():
                return {'error': 'Text cannot be empty'}, 400

        if 'rating' in data:
            rating = data['rating']
            if rating is None or not isinstance(rating, int) or isinstance(rating, bool) or not (1 <= rating <= 5):
                return {'error': 'Rating must be an integer between 1 and 5'}, 400

        try:
            updated_review = facade.update_review(review_id, data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id if hasattr(updated_review.user, 'id') else updated_review.user_id,
                'place_id': updated_review.place.id if hasattr(updated_review.place, 'id') else updated_review.place_id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200