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

    from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')
        text = review_data.get('text', '')

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        if not text.strip():
            raise ValueError("Review text cannot be empty")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(
            text=text,
            rating=rating,
            place_id=place_id,
            user_id=user_id
        )
        return self.review_repo.add(review)

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        rating = review_data.get('rating')
        text = review_data.get('text')

        if text is not None and not text.strip():
            raise ValueError("Review text cannot be empty")
        if rating is not None and not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        if review_id in self.review_repo._storage:
            del self.review_repo._storage[review_id]
            return True
        return False
    def create_place(self, place_data):
        # 
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner (User) not found")

        # 
        place = Place(
            title=place_data['title'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id'],
            description=place_data.get('description', '')
        )
        return self.place_repo.add(place)

    def create_review(self, review_data):
        # 
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
        return self.review_repo.add(review)
