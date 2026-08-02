import unittest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class TestUserValidation(unittest.TestCase):

    def test_valid_user_creation(self):
        """Test creating a user with valid attributes."""
        user = User("John", "Doe", "john.doe@example.com", "password123")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)

    def test_empty_first_name(self):
        """Test validation error when first name is empty."""
        with self.assertRaises(ValueError) as context:
            User("", "Doe", "john@example.com", "password123")
        self.assertIn("first_name is required", str(context.exception))

    def test_invalid_email_format(self):
        """Test validation error when email format is invalid."""
        with self.assertRaises(ValueError) as context:
            User("John", "Doe", "invalid-email-format", "password123")
        self.assertIn("Invalid email format", str(context.exception))

    def test_short_password(self):
        """Test validation error when password length is under 6 characters."""
        with self.assertRaises(ValueError) as context:
            User("John", "Doe", "john@example.com", "12345")
        self.assertIn("Password must be at least 6 characters long", str(context.exception))

    def test_name_too_long(self):
        """Test validation error when name exceeds 50 characters."""
        long_name = "A" * 51
        with self.assertRaises(ValueError) as context:
            User(long_name, "Doe", "john@example.com", "password123")
        self.assertIn("first_name must be under 50 characters", str(context.exception))

class TestAmenityValidation(unittest.TestCase):

    def test_valid_amenity_creation(self):
        """Test creating an amenity with a valid name."""
        amenity = Amenity("Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

    def test_empty_amenity_name(self):
        """Test validation error when amenity name is empty."""
        with self.assertRaises(ValueError):
            Amenity("")

    def test_amenity_name_too_long(self):
        """Test validation error when amenity name exceeds 50 characters."""
        with self.assertRaises(ValueError):
            Amenity("A" * 51)

class TestPlaceValidation(unittest.TestCase):

    def setUp(self):
        self.owner = User(
            "John",
            "Doe",
            "owner@example.com",
            "password123"
        )

    def test_valid_place_creation(self):
        place = Place(
            title="Cozy Apartment",
            description="A nice place",
            price=100,
            latitude=24.7136,
            longitude=46.6753,
            owner=self.owner
        )

        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 100)
        self.assertEqual(place.owner, self.owner)
        self.assertEqual(place.reviews, [])
        self.assertEqual(place.amenities, [])

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            Place(
                title="",
                description="A nice place",
                price=100,
                latitude=24.7136,
                longitude=46.6753,
                owner=self.owner
            )

    def test_title_too_long(self):
        with self.assertRaises(ValueError):
            Place(
                title="A" * 101,
                description="A nice place",
                price=100,
                latitude=24.7136,
                longitude=46.6753,
                owner=self.owner
            )

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            Place(
                title="Cozy Apartment",
                description="A nice place",
                price=-1,
                latitude=24.7136,
                longitude=46.6753,
                owner=self.owner
            )

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place(
                title="Cozy Apartment",
                description="A nice place",
                price=100,
                latitude=100,
                longitude=46.6753,
                owner=self.owner
            )

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            Place(
                title="Cozy Apartment",
                description="A nice place",
                price=100,
                latitude=24.7136,
                longitude=200,
                owner=self.owner
            )
if __name__ == '__main__':
    unittest.main()
