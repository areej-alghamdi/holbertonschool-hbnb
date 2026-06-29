## 1. User Registration Sequence Diagram

```mermaid
sequenceDiagram
    actor Client as User/Client
    participant API as Presentation (API)
    participant Facade as Business Logic (Facade)
    participant Model as User Model
    participant DB as Persistence (DB)

    Client->>API: POST /api/v1/users (Registration Data)
    API->>Facade: register_user(data)
    activate Facade
    Facade->>DB: Check if email exists
    DB-->>Facade: Email is unique
    Facade->>Model: Create new User instance
    Facade->>DB: save(user)
    DB-->>Facade: User saved successfully
    Facade-->>API: Return User Object & HTTP 201
    deactivate Facade
    API-->>Client: HTTP 201 Created (Success Response)
```

## 2. Place Creation Sequence Diagram

```mermaid
sequenceDiagram
    actor Client as User/Client
    participant API as Presentation (API)
    participant Facade as Business Logic (Facade)
    participant UserModel as User Model
    participant DB as Persistence (DB)

    Client->>API: POST /api/v1/places (Place Data & Owner ID)
    API->>Facade: create_place(data)
    activate Facade
    Facade->>DB: Check if owner_id exists
    DB-->>Facade: Owner is valid (Exists)
    Facade->>UserModel: Validate Owner business rules
    Facade->>DB: save(new_place)
    DB-->>Facade: Place saved successfully
    Facade-->>API: Return Place Object & HTTP 201
    deactivate Facade
    API-->>Client: HTTP 201 Created (Success Response)
```

## 3. Review Submission Sequence Diagram

```mermaid
sequenceDiagram
    actor Client as User/Client
    participant API as Presentation (API)
    participant Facade as Business Logic (Facade)
    participant DB as Persistence (DB)

    Client->>API: POST /api/v1/reviews (User ID, Place ID, Rating, Comment)
    API->>Facade: create_review(data)
    activate Facade
    Facade->>DB: Validate user_id exists
    DB-->>Facade: User is valid
    Facade->>DB: Validate place_id exists
    DB-->>Facade: Place is valid
    Facade->>DB: save(new_review)
    DB-->>Facade: Review saved successfully
    Facade-->>API: Return Review Object & HTTP 201
    deactivate Facade
    API-->>Client: HTTP 201 Created (Success Response)
```
## 4. Fetching a List of Places Sequence Diagram

```mermaid
sequenceDiagram
    actor Client as User/Client
    participant API as Presentation (API)
    participant Facade as Business Logic (Facade)
    participant DB as Persistence (DB)

    Client->>API: GET /api/v1/places
    API->>Facade: get_places()
    activate Facade
    Facade->>DB: fetch_all_places()
    DB-->>Facade: Return list of places
    Facade-->>API: Return Places Data & HTTP 200
    deactivate Facade
    API-->>Client: HTTP 200 OK (Success Response with Places List)
```

---

## Explanatory Notes

### 1. User Registration
* **Purpose**: Illustrates the step-by-step process of creating a new user account.
* **Flow**: The request hits the **Presentation Layer (API)**, which triggers the **Business Logic (Facade)** to check if the user's email already exists in the **Persistence Layer (DB)**. Once validated as unique, a new User Model is created and saved successfully.

### 2. Place Creation
* **Purpose**: Visualizes how a user lists a new place in the application.
* **Flow**: The **API** sends the data to the **Facade**. The system verifies the `owner_id` against the **DB** to ensure the owner exists, validates the business rules, and then persists the new place object.

### 3. Review Submission
* **Purpose**: Demonstrates the process of a user submitting a review and rating for a specific place.
* **Flow**: The **Presentation Layer** forwards the payload to the **Business Logic**. The **Facade** cross-checks both the `user_id` and `place_id` in the **Database** to ensure they are valid before saving the review record.

### 4. Fetching a List of Places
* **Purpose**: Shows how the system handles a request to retrieve all place listings.
* **Flow**: The client sends a GET request to the **API**. The **Facade** communicates directly with the **Persistence Layer (DB)** to fetch all stored places and routes the clean data back to the client with an HTTP 200 OK status.
