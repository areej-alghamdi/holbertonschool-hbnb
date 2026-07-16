# HBnB Evolution - Part 2: API & Business Logic Layer

---

## 📝 1. Introduction
Welcome to **HBnB Evolution (Part 2)**! This phase of the project focuses on constructing the foundational architecture of the HBnB platform: the **Business Logic Layer** and the **API Presentation Layer**. 

In this part, we transition from conceptual diagrams to actual software design. By employing Python, Flask, and Flask-RESTx, we construct the core API endpoints that will power our entire application, ensuring seamless integration between users, places, amenities, and reviews.

---

## 🎯 2. Project Vision
Our vision for the HBnB platform is to build a fully decoupled, secure, and highly scalable custom application. 

By applying a **Layered Architecture**, we decouple our core business logic from the specific storage mechanism (in-memory, SQL, etc.) and presentation details (web servers). This guarantees that our platform is:
*   **Scalable:** Easy to add new modules and services without breaking existing ones.
*   **Maintainable:** Every component has one distinct responsibility.
*   **Testable:** The modular logic allows robust automated testing for every component.

---

## 🎓 3. Learning Objectives
By completing this phase of the project, we have successfully achieved the following technical milestones:
*   **Layered Architectural Implementation:** Constructing and maintaining separation between the Presentation, Business Logic, and Persistence Layers.
*   **The Facade Pattern:** Implementing a centralized `ServiceFacade` to coordinate communication between layers and eliminate direct dependencies between different modules.
*   **API Design with Flask-RESTx:** Creating standard, self-documenting RESTful APIs with organized namespaces.
*   **Data Validation & Sanitization:** Building bulletproof domain-level rules to handle bad inputs and edge cases gracefully.

---

## 📂 4. Project Repository Structure
Below is the directory tree for Part 2 of the HBnB project, highlighting our modular design:

```text
part2/
├── app/
│   ├── __init__.py                # App factory & API initialization
│   ├── api/
│   │   ├── __init__.py
│   │   v1/
│   │       ├── __init__.py
│   │       ├── amenities.py       # Amenity API endpoints & models
│   │       ├── places.py          # Place API endpoints, nested owners, & validation
│   │       ├── reviews.py         # Review API endpoints & validations
│   │       └── users.py           # User creation, retrieval, & updates
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py             # Amenity domain entity (inherits from BaseModel)
│   │   ├── base.py                # BaseModel with UUID, timestamps, and core attributes
│   │   ├── place.py               # Place domain entity with linked owner and amenities
│   │   ├── review.py              # Review domain entity referencing user and place
│   │   └── user.py                # User domain entity with strict email & length rules
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py          # Generic In-Memory Repository pattern implementation
│   └── services/
│       ├── __init__.py
│       └── facade.py              # Service Facade orchestrating all domain interconnections
├── run.py                         # Application entrypoint
└── README.md                      # Project documentation (this file!)## Installation & Running


1. Clone the repository:
```
git clone https://github.com/areej-alghamdi/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
```

2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the application:
```
python3 run.py
```

The API will be available at http://127.0.0.1:5000
with automatic Swagger documentation.
# Task 3 - Amenity Endpoints

## Objective
Implement the API endpoints required for managing amenities in the HBnB application, ensuring integration with the Business Logic layer via the Facade pattern. The DELETE operation is not implemented in this part.


## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/v1/amenities/ | Create a new amenity |
| GET | /api/v1/amenities/ | Retrieve all amenities |
| GET | /api/v1/amenities/<amenity_id> | Get amenity by ID |
| PUT | /api/v1/amenities/<amenity_id> | Update an amenity |

## Input Format (POST and PUT)
```json
{
  "name": "Wi-Fi"
}
```

## Output Format
```json
{
  "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "Wi-Fi"
}
```

## Status Codes
- 201 Created — amenity successfully created
- 200 OK — amenity retrieved or updated successfully
- 400 Bad Request — invalid input data 
- 404 Not Found — amenity not found

---

# Task 4 - Place Endpoints

## Objective
Implement the API endpoints needed for managing places in the HBnB application. This includes handling relationships with User (owner) and Amenity, and implementing validation for price, latitude, and longitude. The DELETE operation is not implemented in this part.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/v1/places/ | Create a new place |
| GET | /api/v1/places/ | Retrieve all places |
| GET | /api/v1/places/<place_id> | Get place by ID with owner and amenities |
| PUT | /api/v1/places/<place_id> | Update a place |

## Validation Rules
- price must be a non-negative float
- latitude must be between -90.0 and 90.0
- longitude must be between -180.0 and 180.0
- owner_id must reference an existing User
- amenities must reference existing Amenity IDs

## Input Format (POST)
```json
{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "amenities": []
}
```

## Output Format (GET by ID)
```json
{
  "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  "amenities": [
    {
      "id": "4fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "Wi-Fi"
    }
  ]
}
```

## Status Codes
## Testing (Tasks 3 & 4)

The API was tested manually using the Swagger UI to verify
that each endpoint returns the correct response and status code.

### Task 3 — Amenity endpoints
- Create amenity (POST): returned 201 with the new amenity data
- Retrieve all amenities (GET): returned 200 with the list
- Retrieve amenity by ID (GET): returned 200 with the amenity
- Retrieve with wrong ID: returned 404 "Amenity not found"
- Update amenity (PUT): returned 200 with
  {"message": "Amenity updated successfully"}

### Task 4 — Place endpoints
- Create place with valid owner (POST): returned 201 with
  nested owner details
- Create place with invalid latitude (999): returned 400
  "Latitude must be between -90.0 and 90.0"


###List of status code: 
- 201 Created — place successfully created
- 200 OK — place retrieved or updated successfully
- 400 Bad Request — invalid input data
- 404 Not Found — place, owner, or amenity not found

---
## Task 5: Review Endpoints
 
**Objective:** Implement the API endpoints needed for managing reviews in the HBnB application. This includes full CRUD operations (Create, Read, Update, Delete), integrated with the Business Logic layer via the Facade pattern. Review is the first entity for which the DELETE operation is supported in this part of the project.
 
**Endpoints**
 
| Method | URL | Description |
|---|---|---|
| POST | `/api/v1/reviews/` | Create a new review |
| GET | `/api/v1/reviews/` | Retrieve all reviews |
| GET | `/api/v1/reviews/<review_id>` | Get review by ID |
| PUT | `/api/v1/reviews/<review_id>` | Update a review |
| DELETE | `/api/v1/reviews/<review_id>` | Delete a review |
| GET | `/api/v1/places/<place_id>/reviews` | Get all reviews for a specific place |
 
**Validation Rules**
- `text` cannot be empty
- `rating` must be between 1 and 5
- `user_id` must reference an existing User
- `place_id` must reference an existing Place
**Input Format (POST)**
 
```json
{
  "text": "Great stay, very clean and comfortable.",
  "rating": 5,
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
 
**Output Format**
 
```json
{
  "id": "6fa85f64-5717-4562-b3fc-2c963f66afa6",
  "text": "Great stay, very clean and comfortable.",
  "rating": 5,
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
 
**Status Codes**
 
| Code | Meaning |
|---|---|
| `201 Created` | Review successfully created |
| `200 OK` | Review retrieved, updated, or deleted successfully |
| `400 Bad Request` | Invalid input data |
| `404 Not Found` | Review, user, or place not found |
 
---
 
## Task 6: Testing and Validation
 
**Objective:** Write and run tests for all endpoints developed in previous tasks, apply validation logic, perform thorough black-box testing with cURL and Swagger, and document the results in a testing report.
 
**Scope**
- Basic validation implemented for every attribute across all models (User, Amenity, Place, Review).
- Black-box testing performed using `cURL` and the Swagger UI generated by Flask-RESTx.
- Unit tests written using `unittest` / `pytest`.
- Detailed testing report covering both successful and failed cases.
**Status Codes**
 
| Code | Meaning |
|---|---|
| `201 Created` | Resource successfully created |
| `200 OK` | Resource retrieved or updated successfully |
| `400 Bad Request` | Invalid input / validation failure |
| `404 Not Found` | Resource not found |
 
---
 






## Authors:
-Ahaad AL-Qahtani -Areej Al-Ghamdi -Hadeel Al-Qahatni
