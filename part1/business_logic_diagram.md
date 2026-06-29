# HBnB Application - Class Diagram

This file shows the detailed Class Diagram for the Business Logic layer of the HBnB application, depicting entities, attributes, methods, and relationships.
---

## 1. Business Logic Layer Class Diagram

<img width="802" height="906" alt="unnamed" src="https://github.com/user-attachments/assets/e2abbe06-fe1d-4765-8bf4-cdafdf7497c7" />

## Explanatory Notes

### 1. Core Entities
* **User**: Manages internal account details, authentication processes, and holds standard security features like `password_hash` and state tracking (`is_active`).
* **Place**: Encapsulates data related to the property listing, including explicit coordinates (`longitude`, `latitude`) and structural associations for local queries.
* **Review**: Stores the consumer-driven feedback engine detailing the physical property experience mapped back to the direct users and places.
* **Amenity**: Contains standard global metadata objects for property filters (e.g., WiFi, Pool).

### 2. Structural Relationships & Multiplicities
* **User to Place (`1 --> 0..*`)**: A single unique User can host or own multiple separate Places, while a Place references exactly one specific host owner profile via `owner_id`.
* **User to Review (`1 --> 0..*`)**: An individual User records or authors multiple distinct reviews over their runtime history.
* **Place to Review (`1 --> 0..*`)**: A single property asset holds records for an absolute historical range of public user reviews via `list_reviews()`.
* **Place to Amenity (`0..* --> 0..*`)**: A dynamic Many-to-Many system where physical accommodations can dynamically present multiple amenities, and singular specific amenities populate globally across numerous structural properties.




