from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        # Initialize repository for users
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user after verifying the email is unique."""
        email = user_data.get('email')
        
        # 1. Check if email is already registered
        existing_user = self.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
            
        # 2. Create the user object if email is unique
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=email
        )
        
        # 3. Save to repository
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all registered users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user fields with validation."""
        user = self.get_user(user_id)
        if not user:
            return None
            
        # Update first name
        if 'first_name' in user_data:
            user.first_name = user.validate_name(user_data['first_name'], 'first_name')
            
        # Update last name
        if 'last_name' in user_data:
            user.last_name = user.validate_name(user_data['last_name'], 'last_name')
            
        # Update email and check for uniqueness
        if 'email' in user_data:
            new_email = user_data['email']
            if new_email != user.email and self.get_user_by_email(new_email):
                raise ValueError("Email already registered")
            user.email = user.validate_email(new_email)
            
        # Save updates
        self.user_repo.update(user.id, user_data)
        return user
