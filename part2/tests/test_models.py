import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestModelValidations(unittest.TestCase):

    def setUp(self):
        self.valid_user = User(
            first_name="John", 
            last_name="Doe", 
            email="john.doe@example.com", 
            password="securepassword123"
        )
        self.valid_place = Place(
            title="Cozy Apartment", 
            description="A nice place", 
            price=100.0, 
            latitude=45.0, 
            longitude=90.0, 
            owner=self.valid_user
        )

    def test_review_creation_success(self):
        review = Review(text="Amazing stay!", rating=5, place_id="place-123", user_id="user-123")
        self.assertEqual(review.text, "Amazing stay!")
        self.assertEqual(review.rating, 5)

    def test_review_empty_text_raises_value_error(self):
        with self.assertRaises(ValueError):
            Review(text="   ", rating=5, place_id="place-123", user_id="user-123")

    def test_review_invalid_rating_raises_value_error(self):
        with self.assertRaises(ValueError):
            Review(text="Good", rating=6, place_id="place-123", user_id="user-123")
        with self.assertRaises(ValueError):
            Review(text="Bad", rating=0, place_id="place-123", user_id="user-123")

    def test_user_invalid_email_raises_value_error(self):
        with self.assertRaises(ValueError):
            User(first_name="Jane", last_name="Doe", email="invalid-email", password="123456")

    def test_place_invalid_coords_raises_value_error(self):
        with self.assertRaises(ValueError):
            Place("Hotel", "Desc", 150, latitude=95.0, longitude=45.0, owner=self.valid_user)

if __name__ == '__main__':
    unittest.main()
