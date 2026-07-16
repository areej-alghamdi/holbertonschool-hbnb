import unittest
from app import create_app

class TestHBnBAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "invalid-email-format"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": -10.5,
            "latitude": 34.05,
            "longitude": -118.24,
            "owner_id": "some-user-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_out_of_bounds_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Mountain Cabin",
            "price": 150.0,
            "latitude": 95.0,
            "longitude": 45.0,
            "owner_id": "some-user-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great experience!",
            "rating": 6,
            "user_id": "some-user-id",
            "place_id": "some-place-id"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
