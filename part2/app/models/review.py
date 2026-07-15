from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = place  # Represents the Place Object directly
        self.user = user    # Represents the User Object directly

    def validate_text(self, text):
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("Review text is required")
        return text.strip()

    def validate_rating(self, rating):
        if not isinstance(rating, int):
            try:
                rating = int(rating)
            except (TypeError, ValueError):
                raise ValueError("Rating must be an integer between 1 and 5")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating
