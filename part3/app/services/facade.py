from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # -------------------------
    # User Methods
    # -------------------------
    def create_user(self, user_data):
        email = user_data.get("email")

        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

        user = User(
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            email=email,
            password=user_data.get("password"),
            is_admin=user_data.get("is_admin", False)
        )

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)

        if not user:
            return None

        validated_data = {}

        if "first_name" in user_data:
            first_name = user_data["first_name"]

            if (
                not isinstance(first_name, str)
                or not first_name.strip()
                or len(first_name.strip()) > 50
            ):
                raise ValueError(
                    "First name is required and must not exceed 50 characters"
                )

            validated_data["first_name"] = first_name.strip()

        if "last_name" in user_data:
            last_name = user_data["last_name"]

            if (
                not isinstance(last_name, str)
                or not last_name.strip()
                or len(last_name.strip()) > 50
            ):
                raise ValueError(
                    "Last name is required and must not exceed 50 characters"
                )

            validated_data["last_name"] = last_name.strip()

        if "email" in user_data:
            new_email = user_data["email"]

            existing_user = self.get_user_by_email(new_email)

            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

            validated_data["email"] = new_email

        if "is_admin" in user_data:
            validated_data["is_admin"] = bool(user_data["is_admin"])

        if "password" in user_data:
            password = user_data["password"]

            if not isinstance(password, str) or len(password) < 6:
                raise ValueError(
                    "Password must contain at least 6 characters"
                )

            user.hash_password(password)

        self.user_repo.update(user_id, validated_data)
        return user

    # -------------------------
    # Amenity Methods
    # -------------------------
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")

        if not isinstance(name, str) or not name.strip():
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

        if "name" in amenity_data:
            name = amenity_data["name"]

            if not isinstance(name, str) or not name.strip():
                raise ValueError("Amenity name is required")

            if len(name.strip()) > 50:
                raise ValueError(
                    "Amenity name must be under 50 characters"
                )

            validated_data["name"] = name.strip()

        return self.amenity_repo.update(
            amenity_id,
            validated_data
        )

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # -------------------------
    # Place Methods
    # -------------------------
    def create_place(self, place_data):
        place_data = place_data.copy()

        owner_id = place_data.pop("owner_id", None)
        amenity_ids = place_data.pop("amenities", [])

        if not owner_id:
            raise ValueError("Owner ID is required")

        owner = self.get_user(owner_id)

        if not owner:
            raise ValueError(
                f"Owner with id {owner_id} does not exist"
            )

        amenities = []

        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)

            if not amenity:
                raise ValueError(
                    f"Amenity with id {amenity_id} does not exist"
                )

            amenities.append(amenity)

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )

        place.amenities = amenities

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

        validated_data = {}

        if "title" in place_data:
            validated_data["title"] = place.validate_string(
                place_data["title"],
                "title",
                max_length=100
            )

        if "description" in place_data:
            validated_data["description"] = place_data["description"]

        if "price" in place_data:
            validated_data["price"] = place.validate_price(
                place_data["price"]
            )

        if "latitude" in place_data:
            validated_data["latitude"] = place.validate_latitude(
                place_data["latitude"]
            )

        if "longitude" in place_data:
            validated_data["longitude"] = place.validate_longitude(
                place_data["longitude"]
            )

        if "amenities" in place_data:
            amenities = []

            for amenity_id in place_data["amenities"]:
                amenity = self.get_amenity(amenity_id)

                if not amenity:
                    raise ValueError(
                        f"Amenity with id {amenity_id} does not exist"
                    )

                amenities.append(amenity)

            place.amenities = amenities

        self.place_repo.update(place_id, validated_data)
        return place

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # -------------------------
    # Review Methods
    # -------------------------
    def create_review(self, review_data):
        review_data = review_data.copy()

        place_id = review_data.pop("place_id", None)
        user_id = review_data.pop("user_id", None)

        place = self.get_place(place_id)

        if not place:
            raise ValueError("Place does not exist")

        user = self.get_user(user_id)

        if not user:
            raise ValueError("User does not exist")

        if place.owner.id == user.id:
            raise ValueError("You cannot review your own place")

        existing_reviews = self.get_reviews_by_place(place_id)

        for existing_review in existing_reviews:
            if existing_review.user_id == user_id:
                raise ValueError(
                    "You have already reviewed this place"
                )

        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            place=place,
            user=user
        )

        self.review_repo.add(review)
        place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()

        return [
            review
            for review in reviews
            if review.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)

        if not review:
            return None

        allowed_fields = {"text", "rating"}

        validated_data = {
            key: value
            for key, value in review_data.items()
            if key in allowed_fields
        }

        return self.review_repo.update(
            review_id,
            validated_data
        )

    def delete_review(self, review_id):
        review = self.get_review(review_id)

        if not review:
            return None

        place = self.get_place(review.place_id)

        if (
            place
            and hasattr(place, "reviews")
            and review in place.reviews
        ):
            place.reviews.remove(review)

        return self.review_repo.delete(review_id)
