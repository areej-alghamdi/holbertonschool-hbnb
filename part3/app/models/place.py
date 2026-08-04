from app.models.base_model import BaseModel
from app import db


# Association table for the many-to-many relationship
# between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
    ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
    )

    owner = db.relationship(
        'User',
        back_populates='places'
    )

    reviews = db.relationship(
        'Review',
        back_populates='place',
        cascade='all, delete-orphan',
        lazy=True
    )

    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        lazy='subquery'
    )

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner
    ):
        super().__init__()

        # Basic validation for Place attributes (including max 100 chars for title)
        self.title = self.validate_string(
            title,
            "title",
            max_length=100
        )
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner  # Receives the entire User object

    def validate_string(self, value, field_name, max_length=None):
        """Ensure the string is non-empty and within length limits."""
        if (
            not value
            or not isinstance(value, str)
            or len(value.strip()) == 0
        ):
            raise ValueError(f"{field_name} is required")

        cleaned_value = value.strip()

        if max_length and len(cleaned_value) > max_length:
            raise ValueError(
                f"{field_name} must not exceed "
                f"{max_length} characters"
            )

        return cleaned_value

    def validate_price(self, price):
        """Ensure price is a positive number."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number")
        return price

    def validate_latitude(self, lat):
        """Ensure latitude is within world bounds."""
        if (
            not isinstance(lat, (int, float))
            or not (-90.0 <= lat <= 90.0)
        ):
            raise ValueError(
                "Latitude must be between -90.0 and 90.0"
            )

        return lat

    def validate_longitude(self, lon):
        """Ensure longitude is within world bounds."""
        if (
            not isinstance(lon, (int, float))
            or not (-180.0 <= lon <= 180.0)
        ):
            raise ValueError(
                "Longitude must be between -180.0 and 180.0"
            )

        return lon

    def add_review(self, review):
        """Add review to place."""
        from app.models.review import Review

        if not isinstance(review, Review):
            raise TypeError("review must be a Review")

        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add amenity to place."""
        from app.models.amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity")

        self.amenities.append(amenity)

    def to_dict(self):
        """Return dictionary representation with flattened relationships."""
        data = super().to_dict()
        data["owner_id"] = self.owner_id
        data.pop("owner", None)
        data["reviews"] = [
            review.id for review in self.reviews
        ]
        data["amenities"] = [
            amenity.id for amenity in self.amenities
        ]

        return data
