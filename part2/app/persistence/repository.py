from abc import ABC, abstractmethod

# Abstract Base Class representing the Repository Interface
class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        """Add a new object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its unique ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all stored objects."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an existing object by its ID."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object from the repository."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute name and value."""
        pass


# Concrete implementation of the Repository Interface using in-memory storage
class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            # Delegate update responsibility to the model object itself (Separation of Concerns)
            obj.update(data)
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        # Search the storage for an object with a matching attribute value
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None
