# HBnB Evolution – Part 3

## Description

HBnB Evolution is a backend RESTful API inspired by platforms such as Airbnb.

This third part of the project improves the previous implementation by adding:

* Secure user authentication using JWT.
* Password hashing using Flask-Bcrypt.
* Role-based access control for administrators.
* Ownership-based authorization for places and reviews.
* Persistent data storage using SQLAlchemy.
* SQLite support for development.
* MySQL-ready configuration for production.
* Interactive API documentation using Swagger UI.

The application follows a layered architecture that separates the API, business logic, models, and persistence layers.

---

## Features

### User Management

Users can:

* Register a new account.
* Log in using their email and password.
* Retrieve public user information.
* Update their own account information.

Passwords are securely hashed before being stored and are never returned in API responses.

Administrators have additional permissions, such as managing other users and accessing protected operations.

### Authentication

The application uses JSON Web Tokens, or JWT, for authentication.

After a successful login, the API returns an access token. The token must be included in protected requests using the following header:

```text
Authorization: Bearer <access_token>
```

The token contains:

* The authenticated user's ID.
* The user's administrator status.

### Place Management

Authenticated users can:

* Create a place.
* Update places they own.
* Delete places they own.

Public users can:

* View all places.
* View the details of a specific place.

Administrators can update or delete any place.

### Review Management

Authenticated users can:

* Create a review for a place.
* Update their own reviews.
* Delete their own reviews.

The following rules are applied:

* A user cannot review their own place.
* A user cannot submit more than one review for the same place.
* Only the review creator or an administrator can edit or delete a review.

Public users can view reviews without authentication.

### Amenity Management

The API supports the creation, retrieval, and management of amenities that can be associated with places.

Examples include:

* Wi-Fi
* Swimming pool
* Air conditioning
* Parking

---

## Technologies Used

* Python 3
* Flask
* Flask-RESTx
* Flask-JWT-Extended
* Flask-Bcrypt
* Flask-SQLAlchemy
* SQLAlchemy
* SQLite
* MySQL
* Swagger UI

---

## Project Structure

```text
part3/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── persistence/
│   │   └── repository.py
│   └── services/
│       └── facade.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Architecture

The project uses a layered architecture.

### Presentation Layer

Located inside:

```text
app/api/v1/
```

This layer defines the REST API endpoints and handles HTTP requests and responses.

### Business Logic Layer

Located inside:

```text
app/models/
```

This layer contains the main application entities and their validation rules:

* User
* Place
* Review
* Amenity

### Facade Layer

Located inside:

```text
app/services/facade.py
```

The facade acts as the main communication point between the API layer and the persistence layer.

It centralizes operations such as:

* Creating users.
* Retrieving places.
* Updating reviews.
* Checking email uniqueness.
* Managing relationships between entities.

### Persistence Layer

The persistence layer uses SQLAlchemy to store and retrieve application data.

SQLite is used during development, while the application configuration can be adapted to use MySQL in production.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/holbertonschool-hbnb.git
```

Move into the Part 3 directory:

```bash
cd holbertonschool-hbnb/part3
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask development server:

```bash
python3 run.py
```

The application should run at:

```text
http://127.0.0.1:5000
```

Swagger documentation is available at:

```text
http://127.0.0.1:5000/api/v1/
```

---

## API Authentication

### Register a User

```http
POST /api/v1/users/
```

Example request:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

Example response:

```json
{
  "id": "user-uuid",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_admin": false
}
```

The password is hashed before it is stored and is excluded from the response.

### Log In

```http
POST /api/v1/auth/login
```

Example request:

```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

Example response:

```json
{
  "access_token": "<jwt_access_token>"
}
```

### Using the Token in Swagger

1. Open the Swagger documentation.
2. Click the **Authorize** button.
3. Enter the token using the following format:

```text
Bearer <jwt_access_token>
```

4. Click **Authorize**.

---

## Main API Endpoints

### Authentication

| Method | Endpoint             | Authentication | Description                    |
| ------ | -------------------- | -------------: | ------------------------------ |
| POST   | `/api/v1/auth/login` |             No | Log in and receive a JWT token |

### Users

| Method | Endpoint                  | Authentication | Description           |
| ------ | ------------------------- | -------------: | --------------------- |
| POST   | `/api/v1/users/`          |             No | Register a new user   |
| GET    | `/api/v1/users/`          |             No | Retrieve all users    |
| GET    | `/api/v1/users/<user_id>` |             No | Retrieve a user by ID |
| PUT    | `/api/v1/users/<user_id>` |       Required | Update a user         |

### Places

| Method | Endpoint                    | Authentication | Description            |
| ------ | --------------------------- | -------------: | ---------------------- |
| POST   | `/api/v1/places/`           |       Required | Create a place         |
| GET    | `/api/v1/places/`           |             No | Retrieve all places    |
| GET    | `/api/v1/places/<place_id>` |             No | Retrieve a place by ID |
| PUT    | `/api/v1/places/<place_id>` |    Owner/Admin | Update a place         |
| DELETE | `/api/v1/places/<place_id>` |    Owner/Admin | Delete a place         |

### Reviews

| Method | Endpoint                      | Authentication | Description             |
| ------ | ----------------------------- | -------------: | ----------------------- |
| POST   | `/api/v1/reviews/`            |       Required | Create a review         |
| GET    | `/api/v1/reviews/`            |             No | Retrieve all reviews    |
| GET    | `/api/v1/reviews/<review_id>` |             No | Retrieve a review by ID |
| PUT    | `/api/v1/reviews/<review_id>` |  Creator/Admin | Update a review         |
| DELETE | `/api/v1/reviews/<review_id>` |  Creator/Admin | Delete a review         |

### Amenities

| Method | Endpoint                         |           Authentication | Description            |
| ------ | -------------------------------- | -----------------------: | ---------------------- |
| POST   | `/api/v1/amenities/`             | Depends on configuration | Create an amenity      |
| GET    | `/api/v1/amenities/`             |                       No | Retrieve all amenities |
| GET    | `/api/v1/amenities/<amenity_id>` |                       No | Retrieve an amenity    |
| PUT    | `/api/v1/amenities/<amenity_id>` | Depends on configuration | Update an amenity      |

---

## Authorization Rules

The application applies the following authorization rules:

### Places

* A logged-in user can create a place.
* The authenticated user's ID is automatically assigned as the place owner.
* Only the owner can update or delete the place.
* An administrator can update or delete any place.

### Reviews

* A logged-in user can review a place.
* A user cannot review a place they own.
* A user cannot review the same place more than once.
* Only the review creator can update or delete the review.
* An administrator can update or delete any review.

---

## Example: Create a Place

```http
POST /api/v1/places/
```

Headers:

```text
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request body:

```json
{
  "title": "Modern Apartment",
  "description": "A comfortable apartment in Riyadh",
  "price": 450.0,
  "latitude": 24.7136,
  "longitude": 46.6753,
  "amenities": []
}
```

The authenticated user's ID is automatically used as the owner ID.

---

## Example: Create a Review

```http
POST /api/v1/reviews/
```

Headers:

```text
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request body:

```json
{
  "text": "A clean and comfortable place",
  "rating": 5,
  "place_id": "<place_id>"
}
```

---

## Testing with cURL

### Log In

```bash
curl -X POST \
"http://127.0.0.1:5000/api/v1/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john@example.com",
  "password": "securepassword"
}'
```

### Create a Place

```bash
curl -X POST \
"http://127.0.0.1:5000/api/v1/places/" \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Modern Apartment",
  "description": "A comfortable apartment in Riyadh",
  "price": 450,
  "latitude": 24.7136,
  "longitude": 46.6753,
  "amenities": []
}'
```

### Update a Review

```bash
curl -X PUT \
"http://127.0.0.1:5000/api/v1/reviews/<review_id>" \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{
  "text": "Updated review text",
  "rating": 4
}'
```

---

## HTTP Status Codes

The API uses the following common HTTP status codes:

| Status Code | Meaning                                               |
| ----------: | ----------------------------------------------------- |
|       `200` | Request completed successfully                        |
|       `201` | Resource created successfully                         |
|       `400` | Invalid request or validation error                   |
|       `401` | Authentication is required or credentials are invalid |
|       `403` | The user does not have permission                     |
|       `404` | Resource not found                                    |
|       `500` | Internal server error                                 |

---

## Security

The application includes several security measures:

* Passwords are hashed using Flask-Bcrypt.
* Plain-text passwords are never stored.
* Passwords are excluded from API responses.
* Protected endpoints require JWT authentication.
* JWT claims are used to identify administrators.
* Ownership checks prevent users from modifying resources belonging to other users.
* Users cannot review their own places.
* Duplicate reviews are prevented.

---

## Database

During development, the application uses SQLite.

The database configuration is defined in:

```text
config.py
```

SQLAlchemy models define the relationships between users, places, reviews, and amenities.

Main relationships include:

* One user can own multiple places.
* One user can create multiple reviews.
* One place can contain multiple reviews.
* One place can contain multiple amenities.
* Deleting a user can remove their related places and reviews depending on the configured cascade rules.

---

## Authors

* Hadeel Alqahtani
* Areej Alghamdi
* Ahd Alqhtani

---

## License

This project was developed as part of the Holberton School curriculum.
