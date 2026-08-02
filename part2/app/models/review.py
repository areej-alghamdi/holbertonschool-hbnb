from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    def validate_text(self, text):
        if not text or not str(text).strip():
            raise ValueError("Text is required and cannot be empty")
        return str(text)

    def validate_rating(self, rating):
        if rating is None or not isinstance(rating, int) or isinstance(rating, bool) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def validate_place(self, place):
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")
        return place

    def validate_user(self, user):
        if not isinstance(user, User):
            raise ValueError("user must be a valid User instance")
        return user

    @property
    def place_id(self):
        return self.place.id if hasattr(self.place, 'id') else self.place

    @property
    def user_id(self):
        return self.user.id if hasattr(self.user, 'id') else self.user

    def update(self, data):
        if 'text' in data:
            self.text = self.validate_text(data['text'])
        if 'rating' in data:
            self.rating = self.validate_rating(data['rating'])
        self.save()
