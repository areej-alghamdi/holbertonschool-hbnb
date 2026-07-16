import unittest
import json
from app import create_app
from app.services import facade

class TestHBnBValidationAndAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

        self.user = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })

    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email-format"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Nice Villa",
            "price": -10.0,
            "latitude": 45.0,
            "longitude": 90.0,
            "owner_id": self.user.id
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
