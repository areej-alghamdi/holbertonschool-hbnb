```mermaid
classDiagram
    class BaseModel {
        +UUID4 id
        +DateTime created_at
        +DateTime updated_at
        +save() void
        +update(dict data) void
    }

    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register() Boolean
        +login() Boolean
        +update_profile(dict data) void
    }

    class Place {
        +String title
        +String description
        +Float price_per_night
        +Float latitude
        +Float longitude
        +UUID4 owner_id
        +add_amenity(Amenity amenity) void
        +remove_amenity(UUID4 amenity_id) void
        +get_reviews() List~Review~
    }

    class Review {
        +UUID4 place_id
        +UUID4 user_id
        +int rating
        +String comment
        +edit_comment(String new_comment) void
    }

    class Amenity {
        +String name
        +String description
    }

    %% Inheritance (Generalization)
    BaseModel <|-- User : Inheritance
    BaseModel <|-- Place : Inheritance
    BaseModel <|-- Review : Inheritance
    BaseModel <|-- Amenity : Inheritance

    %% Relationships and Multiplicities
    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" *-- "0..*" Review : contains
    Place "0..*" --> "0..*" Amenity : has





## Business Logic Layer Description

### 1. Core Entities
* **BaseModel**: The parent class that enforces system-wide consistency. It provides every entity with a unique identifier (`id` via UUID4) and tracking timestamps (`created_at`, `updated_at`).
* **User**: Represents any system user (Guest, Host, or Admin). It contains credentials and profile management logic.
* **Place**: Represents the rental property listed by a host. It stores property details, location, and pricing.
* **Review**: Stores feedback and ratings (1-5) left by users for specific properties.
* **Amenity**: Represents features available at a property (e.g., Wi-Fi, Pool).

### 2. Relationships & Business Rules
* **Inheritance**: `User`, `Place`, `Review`, and `Amenity` inherit from `BaseModel` to reuse lifecycle attributes and save/update methods without code duplication.
* **User to Place (1 to Many)**: A `User` can own zero or multiple properties, but every `Place` must have exactly one owner.
* **User to Review (1 to Many)**: A `User` can author multiple reviews, but each `Review` belongs to exactly one user.
* **Place to Review (Composition)**: A `Review` cannot exist without a `Place`. If a `Place` is deleted, all its associated reviews are cascade-deleted.
* **Place to Amenity (Many to Many)**: A `Place` can have multiple amenities, and an `Amenity` can be linked to multiple places.
