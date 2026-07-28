import unittest
from app.models.user import User

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

if __name__ == '__main__':
    unittest.main()