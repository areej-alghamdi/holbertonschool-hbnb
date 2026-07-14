from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- User Methods ---
    def create_user(self, user_data):
        email = user_data.get("email")
        if self.user_repo.get_by_attribute("email", email):
            raise ValueError("Email already exists")
        
        # Explicitly building the User object with the password field
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=email,
            password=user_data.get('password')
        )
        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, user_data):
        # Prevent email duplication on update if email is being changed
        if "email" in user_data:
            existing_user = self.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already exists")
        return self.user_repo.update(user_id, user_data)
    