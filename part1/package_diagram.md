# HBnB Application - Package Diagram

This diagram shows the three-layer architecture of the HBnB application
and how the layers communicate via the Facade Pattern.

```mermaid
graph TD
    subgraph Presentation[" Presentation Layer"]
        direction TB
        API["<b>REST API</b><br/>──────────────<br/>+ register_user()<br/>+ create_place()<br/>+ submit_review()<br/>+ get_places()"]
        Services["<b>Services</b><br/>──────────────<br/>+ handle_request()<br/>+ validate_input()<br/>+ format_response()"]
        Auth["<b>Auth & Session</b><br/>──────────────<br/>+ login()<br/>+ logout()<br/>+ validate_token()"]
    end

    subgraph Business["  Business Logic Layer"]
        direction TB
        User["<b>User Model</b><br/>──────────────<br/>- id<br/>- first_name<br/>- last_name<br/>- email<br/>──────────────<br/>+ register()<br/>+ update_profile()<br/>+ delete()"]
        Place["<b>Place Model</b><br/>──────────────<br/>- id<br/>- title<br/>- price<br/>- latitude<br/>- longitude<br/>──────────────<br/>+ create()<br/>+ update()<br/>+ delete()"]
        Review["<b>Review Model</b><br/>──────────────<br/>- id<br/>- rating<br/>- comment<br/>──────────────<br/>+ create()<br/>+ update()<br/>+ delete()"]
        Amenity["<b>Amenity Model</b><br/>──────────────<br/>- id<br/>- name<br/>- description<br/>──────────────<br/>+ create()<br/>+ update()<br/>+ delete()"]
    end

    subgraph Persistence["  Persistence Layer"]
        direction TB
        Repo["<b>Repository</b><br/>──────────────<br/>+ add()<br/>+ get()<br/>+ update()<br/>+ delete()"]
        DB["<b>Database Access</b><br/>──────────────<br/>+ execute_query()<br/>+ commit()<br/>+ rollback()"]
        Storage["<b>Storage Engine</b><br/>──────────────<br/>+ connect()<br/>+ disconnect()<br/>+ backup()"]
    end

    Presentation -->|"Facade Pattern"| Business
    Business -->|"Facade Pattern"| Persistence
```





## Explanatory Notes

### 1. Layers Overview

* **Presentation Layer:** This is the entry point of the application. It handles all 
incoming HTTP requests from the user through the REST API, manages services for request 
handling, and validates user authentication via session tokens.

* **Business Logic Layer:** This is the brain of the application. It contains the core 
models and rules that drive the system:
    * **User** - manages user registration and profile updates
    * **Place** - manages property listings and their details
    * **Review** - manages ratings and comments left by users
    * **Amenity** - manages features that can be associated with places

* **Persistence Layer:** This layer is responsible for storing and retrieving all 
application data. It contains the repository for CRUD operations, database access 
for SQL and ORM queries, and the storage engine that connects to the file or 
database backend.

### 2. Communication Between Layers

The layers communicate through the **Facade Pattern**, which acts as a simplified 
interface between each layer:

* The **Presentation Layer** never accesses the database directly. Instead it calls 
the Facade to reach the Business Logic Layer.
* The **Business Logic Layer** never writes to the database directly. Instead it calls 
the Facade to reach the Persistence Layer.
* This ensures each layer has one clear responsibility and changes in one layer do 
not break the others.


## Facade Pattern Flow

This diagram shows how the Facade Pattern controls 
communication between the layers step by step.

```mermaid
sequenceDiagram
    participant U as User
    participant P as Presentation Layer
    participant F as Facade
    participant B as Business Logic Layer
    participant DB as Persistence Layer

    U->>P: Send Request
    P->>F: Call Facade
    F->>B: Forward to Business Logic
    B->>F: Apply Rules
    F->>DB: Save/Load Data
    DB->>F: Return Data
    F->>P: Return Result
    P->>U: Send Response
```

### 3. The Facade Pattern

The Facade Pattern acts as the communication bridge between the layers:

* The **User** never talks directly to the database.
* The **Presentation Layer** sends requests through the Facade 
  to reach the Business Logic Layer.
* The **Business Logic Layer** sends data through the Facade 
  to reach the Persistence Layer.
* Each layer only knows about the layer directly next to it.
* This keeps the code clean, organized, and easy to maintain.
* If we change the database in the future, only the Persistence 
  Layer needs to change — the other layers are not affected.

  
