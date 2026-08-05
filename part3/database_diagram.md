# HBnB Database ER Diagram

```mermaid
erDiagram
    USER {
        CHAR_36 id PK
        VARCHAR_255 first_name
        VARCHAR_255 last_name
        VARCHAR_255 email UK
        VARCHAR_255 password
        BOOLEAN is_admin
    }

    PLACE {
        CHAR_36 id PK
        VARCHAR_255 title
        TEXT description
        DECIMAL_10_2 price
        FLOAT latitude
        FLOAT longitude
        CHAR_36 owner_id FK
    }

    REVIEW {
        CHAR_36 id PK
        TEXT text
        INT rating
        CHAR_36 user_id FK
        CHAR_36 place_id FK
    }

    AMENITY {
        CHAR_36 id PK
        VARCHAR_255 name UK
    }

    PLACE_AMENITY {
        CHAR_36 place_id PK, FK
        CHAR_36 amenity_id PK, FK
    }

    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : includes
```

## Relationship Summary

- A user can own multiple places, while each place belongs to one user.
- A user can write multiple reviews, while each review belongs to one user.
- A place can receive multiple reviews, while each review belongs to one place.
- Places and amenities have a many-to-many relationship through the `PLACE_AMENITY` association table.

## Database Constraints

- User emails are unique.
- Amenity names are unique.
- A user can submit only one review per place.
- Review ratings must be between 1 and 5.
- The combination of `place_id` and `amenity_id` forms the composite primary key of `PLACE_AMENITY`.

## Exported Diagram

![HBnB ER Diagram](docs/hbnb_er_diagram.png)
