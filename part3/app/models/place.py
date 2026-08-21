from app.models.base_model import BaseModel
from app import db


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

        self.title = self.validate_string(
            title,
            "title",
            max_length=100
        )
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner

    def validate_string(self, value, field_name, max_length=None):
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
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number")
        return price

    def validate_latitude(self, lat):
        if (
            not isinstance(lat, (int, float))
            or not (-90.0 <= lat <= 90.0)
        ):
            raise ValueError(
                "Latitude must be between -90.0 and 90.0"
            )

        return lat

    def validate_longitude(self, lon):
        if (
            not isinstance(lon, (int, float))
            or not (-180.0 <= lon <= 180.0)
        ):
            raise ValueError(
                "Longitude must be between -180.0 and 180.0"
            )

        return lon

    def add_review(self, review):
        from app.models.review import Review

        if not isinstance(review, Review):
            raise TypeError("review must be a Review")

        self.reviews.append(review)

    def add_amenity(self, amenity):
        from app.models.amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity")

        self.amenities.append(amenity)

    def to_dict(self):
        data = super().to_dict()
        data["owner_id"] = self.owner_id
        data.pop("owner", None)
        data["reviews"] = [
            review.to_dict() for review in self.reviews
        ]
        data["amenities"] = [
            amenity.to_dict() for amenity in self.amenities
        ]

        return data
