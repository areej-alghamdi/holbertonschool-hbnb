from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        # Initialize the in-memory repository for handling user data
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user after validating their data and checking for duplicates."""
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email')
        )
        
        # Ensure the email is unique before saving the user
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("Email already registered")
            
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user from the repository by their ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find a user in the repository using their email address."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Return a list of all registered users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user's attributes with validation checks."""
        user = self.get_user(user_id)
        if not user:
            return None
            
        # Update and validate first name if provided
        if 'first_name' in user_data:
            user.first_name = user.validate_name(user_data['first_name'], 'first_name')
            
        # Update and validate last name if provided
        if 'last_name' in user_data:
            user.last_name = user.validate_name(user_data['last_name'], 'last_name')
            
        # Update, validate, and check uniqueness for the new email if provided
        if 'email' in user_data:
            new_email = user_data['email']
            if new_email != user.email and self.get_user_by_email(new_email):
                raise ValueError("Email already registered")
            user.email = user.validate_email(new_email)
            
        self.user_repo.update(user.id, user_data)
        return user
