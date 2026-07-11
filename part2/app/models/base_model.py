import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        # Generate a unique ID and set creation/update timestamps
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the update timestamp whenever the object changes."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes based on a provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()
