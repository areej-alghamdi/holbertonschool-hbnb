from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    # -------------------------
    # User Methods
    # -------------------------
    def create_user(self, user_data):
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password')
        )
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("Email already registered")
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        
        validated_data = {}
        if 'first_name' in user_data:
            validated_data['first_name'] = user.validate_name(user_data['first_name'], 'first_name')
        if 'last_name' in user_data:
            validated_data['last_name'] = user.validate_name(user_data['last_name'], 'last_name')
        if 'email' in user_data:
            new_email = user_data['email']
            if new_email != user.email and self.get_user_by_email(new_email):
                raise ValueError("Email already registered")
            validated_data['email'] = user.validate_email(new_email)
            
        self.user_repo.update(user.id, validated_data)
        return user

    # -------------------------
    # Amenity Methods
    # -------------------------
    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Amenity name is required")
        amenity = Amenity(name=name.strip())
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        validated_data = {}
        if 'name' in amenity_data:
            name = amenity_data['name']
            if not name or not isinstance(name, str) or len(name.strip()) == 0:
                raise ValueError("Amenity name is required")
            validated_data['name'] = name.strip()
            
        self.amenity_repo.update(amenity_id, validated_data)
        return amenity

    # -------------------------
    # Place Methods
    # -------------------------
    def create_place(self, place_data):
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner
        )
        
        amenity_ids = place_data.get('amenities', [])
        amenities_objects = []
        for a_id in amenity_ids:
            amenity = self.get_amenity(a_id)
            if amenity:
                amenities_objects.append(amenity)
                
        place.amenities = amenities_objects
        place.amenity_ids = amenity_ids
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get_place(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        validated_data = {}
        if 'title' in place_data:
            validated_data['title'] = place.validate_string(place_data['title'], 'title')
        if 'description' in place_data:
            validated_data['description'] = place_data['description']
        if 'price' in place_data:
            validated_data['price'] = place.validate_price(place_data['price'])
        if 'latitude' in place_data:
            validated_data['latitude'] = place.validate_latitude(place_data['latitude'])
        if 'longitude' in place_data:
            validated_data['longitude'] = place.validate_longitude(place_data['longitude'])
            
        if 'amenities' in place_data:
            amenity_ids = place_data['amenities']
            amenities_objects = []
            for a_id in amenity_ids:
                amenity = self.get_amenity(a_id)
                if amenity:
                    amenities_objects.append(amenity)
            place.amenities = amenities_objects
            place.amenity_ids = amenity_ids

        self.place_repo.update(place_id, validated_data)
        return place
       # --- Review Operations ---
    def create_review(self, review_data):
        """Create a review for a place.

        Takes a single review_data dict (matching the pattern used by
        every other create_* method) -- place_id/user_id are read out
        of it internally, not passed as separate arguments.

        Validates that both the place and the user exist before
        creating the review.
        """
        place_id = review_data.get('place_id')
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place does not exist")

        user_id = review_data.get('user_id')
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User does not exist")

        # Create review with the actual Place and User objects
        review_data_copy = review_data.copy()
        review_data_copy.pop('user_id', None)
        review_data_copy.pop('place_id', None)
        review_data_copy['user'] = user
        review_data_copy['place'] = place

        review = Review(**review_data_copy)
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        """Fetch a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """List all reviews for a specific place."""
        reviews = self.review_repo.get_all()
        return [r for r in reviews if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update an existing review.

        Only text/rating are updatable through this endpoint -- place
        and user are fixed at creation time, so place_id/user_id are
        never passed to review.update() even if a client sends them.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None
        allowed = {'text', 'rating'}
        review.update({k: v for k, v in review_data.items() if k in allowed})
        return review

    def delete_review(self, review_id):
        """Delete a review by ID, also unlinking it from its place."""
        review = self.review_repo.get(review_id)
        if review:
            place = self.place_repo.get(review.place_id)
            if place and review in place.reviews:
                place.reviews.remove(review)
        self.review_repo.delete(review_id)
