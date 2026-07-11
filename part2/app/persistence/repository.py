import uuid
from datetime import datetime

class InMemoryRepository:
    def __init__(self):
        # Using a simple dictionary to save data in memory for now
        self._storage = {}

    def add(self, obj):
        # Adding the object to our dictionary using its ID as the key
        self._storage[obj.id] = obj

    def get(self, obj_id):
        # Looking up the object by its unique ID
        return self._storage.get(obj_id)

    def get_all(self):
        # Turning the dictionary values into a list to return everything
        return list(self._storage.values())

    def update(self, obj_id, data):
        # Finding the object first, then updating its attributes dynamically
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            obj.updated_at = datetime.now()
        return obj

    def delete(self, obj_id):
        # Deleting the object from the dictionary if it exists
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr, value):
        # Searching inside storage for a specific field, like checking an email
        for obj in self._storage.values():
            if getattr(obj, attr, None) == value:
                return obj
        return None
