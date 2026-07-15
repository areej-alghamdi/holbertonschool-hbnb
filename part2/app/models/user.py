from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        # Validate inputs before assigning them to the object
        self.first_name = self.validate_name(first_name, "first_name")
        self.last_name = self.validate_name(last_name, "last_name")
        self.email = self.validate_email(email)
        self.password = self.validate_password(password)  # validated password
        self.is_admin = is_admin

    def validate_name(self, name, field_name):
        """Ensure the name is a non-empty string and within length limits."""
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError(f"{field_name} is required")
        if len(name) > 50:
            raise ValueError(f"{field_name} must be under 50 characters")
        return name.strip()

    def validate_email(self, email):
        """Basic email format validation."""
        if not email or not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email format")
        return email.strip()

    def validate_password(self, password):
        """Ensure the password is secure and not empty."""
        if not password or not isinstance(password, str) or len(password.strip()) == 0:
            raise ValueError("Password is required")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password
