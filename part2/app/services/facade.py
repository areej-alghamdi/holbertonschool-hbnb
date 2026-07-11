from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        # Creating the user repository to manage data inside the facade
        self.user_repo = InMemoryRepository()
