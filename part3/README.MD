# HBnB Evolution - API & Business Logic Layer

---

## 📝 1. Overview
**HBnB Evolution** is a modular, layered, and scalable web application, secure, and highly scalable custom web application inspired by the core functionalities of AirBnB. 

This phase of the project (Part 2) focuses on building the core **Business Logic Layer** and establishing the **API Presentation Layer** using Python, Flask, and Flask-RESTx. Rather than direct database communication, the application utilizes a modular, layered architecture coordinated by a centralized Facade pattern to handle data management, business rules, and validation seamlessly.

---

## 🚀 2. Key Features

Our application manages the entire ecosystem of a rental platform through four core domains:

*   **User Management:** Registering, retrieving, and updating user profiles with strict email validation.
*   **Place & Accommodation Directory:** Creating and managing listings with physical validations (such as coordinates and prices) and linking them to their respective owners.
*   **Amenity Catalog:** Administering a customizable list of amenities (like Wi-Fi, Pool, Air Conditioning) that can be dynamically linked to any listed place.
*   **Review System:** Allowing users to leave reviews and ratings (from 1 to 5 stars) on specific places, ensuring robust relational integrity.

---

## 🏗️ 3. Architecture & Design Patterns

The backend of HBnB is structured following strict software engineering principles:

```text
  +-------------------------------------------------------------+
  |                      Presentation Layer                     |
  |               (Flask-RESTx API / Swagger UI)                |
  +------------------------------+------------------------------+
                                 |
                                 v
  +-------------------------------------------------------------+
  |                     Business Logic Layer                    |
  |            (Service Facade & Domain Model Rules)            |
  +------------------------------+------------------------------+
                                 |
                                 v
  +-------------------------------------------------------------+
  |                      Persistence Layer                      |
  |                (In-Memory Repository Pattern)               |
  +-------------------------------------------------------------+
```

### The Facade Pattern
To avoid tight coupling between our API endpoints and our database/models, we implemented the Facade Pattern via ServiceFacade. All presentation-layer requests communicate exclusively with this facade, which manages interaction with the underlying models and repositories.

## 📋 4. Business & Validation Rules

To safeguard the application's data integrity, the following rules are strictly enforced at the domain level:

| Model | Attribute / Field | Validation Rule & Requirement |
| :--- | :--- | :--- |
| **User** | Email | Must be unique, required, and follow a valid email format. |
| **User** | First/Last Name | Required; maximum length of 50 characters. |
| **Place** | Title | Required; cannot be empty. |
| **Place** | Price | Must be a positive value (greater than or equal to 0). |
| **Place** | Latitude / Longitude | Coordinates must fall within physical boundaries: Latitude (`-90.0` to `90.0`), Longitude (`-180.0` to `180.0`). |
| **Place** | Owner | Must point to a valid, existing User inside the system. |
| **Amenity** | Name | Required; cannot be empty. |
| **Review** | Text | Required; cannot be empty. |
| **Review** | Rating | Must be an integer between 1 and 5. |
| **Review** | User & Place | Must reference a valid, existing User and an existing Place. |

## 🔌 5. Unified API Endpoint Reference

The RESTful API provides a standard interface for all operations. *(Note: DELETE is currently supported for Reviews).*

| Section | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Users** | `POST` | `/api/v1/users/` | Register a new user |
| | `GET` | `/api/v1/users/` | Retrieve a list of all users |
| | `GET` | `/api/v1/users/<user_id>` | Get details of a specific user |
| | `PUT` | `/api/v1/users/<user_id>` | Update user profile information |
| **Amenities** | `POST` | `/api/v1/amenities/` | Create a new amenity |
| | `GET` | `/api/v1/amenities/` | List all available amenities |
| | `GET` | `/api/v1/amenities/<amenity_id>` | Get details of a specific amenity |
| | `PUT` | `/api/v1/amenities/<amenity_id>` | Update amenity details |
| **Places** | `POST` | `/api/v1/places/` | List a new place |
| | `GET` | `/api/v1/places/` | List all available places |
| | `GET` | `/api/v1/places/<place_id>` | Get detailed info about a place (with owner & amenities) |
| | `PUT` | `/api/v1/places/<place_id>` | Update place listing details |
| **Reviews** | `POST` | `/api/v1/reviews/` | Leave a review for a place |
| | `GET` | `/api/v1/reviews/` | List all reviews |
| | `GET` | `/api/v1/reviews/<review_id>` | Get a specific review by ID |
| | `PUT` | `/api/v1/reviews/<review_id>` | Edit a review |
| | `DELETE` | `/api/v1/reviews/<review_id>` | Delete a review from the system |
| | `GET` | `/api/v1/places/<place_id>/reviews` | Retrieve all reviews linked to a specific place |

## 🛠️ 6. Installation & Running

Follow these steps to set up and run the HBnB project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/areej-alghamdi/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
```

### 2. Configure Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python3 run.py
```

The server will start at:

```text
http://127.0.0.1:5000
```

Swagger documentation is available at:

```text
http://127.0.0.1:5000/
```

---

## 🤝 Authors & Contributors

This project is built and maintained by:

*   **Ahaad Al-Qahtani**
*   **Areej Al-Ghamdi**
*   **Hadeel Al-Qahtani**

