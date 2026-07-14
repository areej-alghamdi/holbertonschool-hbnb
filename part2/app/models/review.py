from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = place  # Receives the entire Place object
        self.user = user    # Receives the entire User object

    def validate_text(self, text):
        """Ensure review text is not empty."""
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("Review text is required")
        return text.strip()

    def validate_rating(self, rating):
        """Ensure rating is an integer between 1 and 5."""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating
