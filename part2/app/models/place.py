from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        # Basic validation for Place attributes
        self.title = self.validate_string(title, "title")
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner  # Receives the entire User object instead of just owner_id

    def validate_string(self, value, field_name):
        """Ensure the string is non-empty."""
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required")
        return value.strip()

    def validate_price(self, price):
        """Ensure price is a positive number."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number")
        return price

    def validate_latitude(self, lat):
        """Ensure latitude is within world bounds."""
        if not isinstance(lat, (int, float)) or not (-90.0 <= lat <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        return lat

    def validate_longitude(self, lon):
        """Ensure longitude is within world bounds."""
        if not isinstance(lon, (int, float)) or not (-180.0 <= lon <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return lon
