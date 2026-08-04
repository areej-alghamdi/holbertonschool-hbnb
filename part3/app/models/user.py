from app import db, bcrypt
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship(
        'Place',
        back_populates='owner',
        cascade='all, delete-orphan',
        lazy=True
    )

    reviews = db.relationship(
        'Review',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __init__(self, password=None, **kwargs):
        super().__init__(**kwargs)

        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(
            self.password,
            password
        )
