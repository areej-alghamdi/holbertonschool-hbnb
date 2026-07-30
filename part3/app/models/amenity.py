from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    def validate_name(self, name):
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Amenity name is required")
        if len(name.strip()) > 50:
            raise ValueError("Amenity name must be under 50 characters")
        return name.strip()
