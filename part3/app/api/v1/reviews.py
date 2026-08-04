from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade
from flask import request

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(
        required=True,
        description='Text of the review'
    ),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
    ),
    'place_id': fields.String(
        required=True,
        description='ID of the place'
    )
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(
        required=False,
        description='Updated text of the review'
    ),
    'rating': fields.Integer(
        required=False,
        description='Updated rating of the place (1-5)'
    )
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Bad request')
    @api.response(404, 'Place not found')
    def post(self):
        """Register a new review"""
        current_user_id = get_jwt_identity()
        review_data = api.payload.copy()
        place_id = review_data.get('place_id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # التحقق من أن المستخدم لا يقيّم مكانه الخاص
        owner_id = (
            place.owner.id
            if hasattr(place.owner, 'id')
            else place.owner_id
        )

        if str(owner_id) == str(current_user_id):
            return {
                'error': 'You cannot review your own place'
            }, 400

        # التحقق من عدم التكرار
        all_reviews = facade.get_reviews_by_place(place_id)

        for review in all_reviews:
            review_user_id = (
                review.user.id
                if hasattr(review.user, 'id')
                else review.user_id
            )

            if str(review_user_id) == str(current_user_id):
                return {
                    'error': 'You have already reviewed this place'
                }, 400

        review_data['user_id'] = current_user_id

        try:
            new_review = facade.create_review(review_data)

            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': current_user_id,
                'place_id': place_id
            }, 201

        except ValueError as error:
            return {'error': str(error)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews (Public)"""
        reviews = facade.get_all_reviews()

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }
            for review in reviews
        ], 200


@api.route('/<string:review_id>')
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
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid review data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (Only creator or admin can modify)"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        review_user_id = (
            review.user.id
            if hasattr(review.user, 'id')
            else review.user_id
        )

        if (
            not is_admin
            and str(review_user_id) != str(current_user_id)
        ):
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_review = facade.update_review(
                review_id,
                api.payload
            )

            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id
            }, 200

        except ValueError as error:
            return {'error': str(error)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (Only creator or admin can delete)"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        review_user_id = (
            review.user.id
            if hasattr(review.user, 'id')
            else review.user_id
        )

        if (
            not is_admin
            and str(review_user_id) != str(current_user_id)
        ):
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)

        return {
            'message': 'Review deleted successfully'
        }, 200
