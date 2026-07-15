from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

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
        if 'first_name' in user_data:
            user.first_name = user.validate_name(user_data['first_name'], 'first_name')
        if 'last_name' in user_data:
            user.last_name = user.validate_name(user_data['last_name'], 'last_name')
        if 'email' in user_data:
            new_email = user_data['email']
            if new_email != user.email and self.get_user_by_email(new_email):
                raise ValueError("Email already registered")
            user.email = user.validate_email(new_email)
        self.user_repo.update(user.id, user_data)
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
        if 'name' in amenity_data:
            name = amenity_data['name']
            if not name or not isinstance(name, str) or len(name.strip()) == 0:
                raise ValueError("Amenity name is required")
            amenity.name = name.strip()
        self.amenity_repo.update(amenity_id, amenity_data)
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
        place.owner_id = owner.id
        place.amenity_ids = place_data.get('amenities', [])
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']
        if 'amenity_ids' in place_data:
            place.amenity_ids = place_data['amenity_ids']
        self.place_repo.update(place_id, place_data)
        return place

    # -------------------------
    # Review Methods
    # -------------------------
    def create_review(self, review_data):
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,  # Directly assign the Place Object
            user=user     # Directly assign the User Object
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        all_reviews = self.get_all_reviews()
        return [r for r in all_reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review.validate_text(review_data['text'])
        if 'rating' in review_data:
            review.rating = review.validate_rating(review_data['rating'])
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
