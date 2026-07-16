from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text: str, rating: int, place_id: str, user_id: str):
        super().__init__()
        if not text or not text.strip():
            raise ValueError("Review text cannot be empty")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not place_id:
            raise ValueError("place_id is required")
        if not user_id:
            raise ValueError("user_id is required")

        self.text = text.strip()
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
