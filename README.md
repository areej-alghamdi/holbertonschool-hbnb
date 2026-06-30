# holbertonschool-hbnb
HBnB Evolution project

# Part 1 - Technical Documentation

## HBnB Evolution - Application Architecture

---

## Overview

## This document provides the technical documentation for the HBnB Evolution application.
A simplified HBnB-like platform. It covers the overall architecture, the detailed
design of the business logic, and the interactions within the system.

---

## Task 0 - High-Level Package Diagram

### Architecture Overview

The HBnB Evolution application follows a **three-layer architecture** (Zoom out):

1. **Presentation Layer**
2. **Business Logic Layer**
3. **Persistence Layer**

Each layer communicates with the one directly below it through the **Facade Pattern**.
You Can not skip anylayer.
---

### Layer Descriptions

#### 1. Presentation Layer
- **Responsibility:** Handles all user-facing interactions.
- **Components:**
  - REST API (routes and endpoints)
  - Services (request handling)
  - Auth / Session (token validation)
- **Rule:** This layer does NOT contain business rules such as (Data validation and Entity Relationship Rules),and does NOT access the database directly.

#### 2. Business Logic Layer
- **Responsibility:** Contains the core models and rules of the application.
- **Components:**
  - **User** - handles registration and profile updates
  - **Place** - handles property listings and management
  - **Review** - handles ratings and comments
  - **Amenity** - handles features associated with places
- **Rule:** This layer does NOT know about HTTP or the database. It only applies business rules.

#### 3. Persistence Layer
- **Responsibility:** Stores and retrieves all data (The complex subsystem)
- **Components:**
  - Repository (CRUD operations)
  - Database Access (SQL / ORM queries)
  - Storage Engine (file or database backend)
- **Rule:** This layer does NOT apply rules. It only saves and loads data.

---

### The Facade Pattern

The **Facade Pattern** acts as a simplified interface between layers (The complex subsystem)
- The Presentation Layer calls the Facade to reach the Business Logic Layer.
- The Business Logic Layer calls the Facade to reach the Persistence Layer.
- No layer skips another. This keeps the code organized and easy to maintain.
-The Facade layer hides this complexity from the Service or API layer, so the rest of the application doesn't need to know how or where data is being saved.

---

### Package Diagram

See the file `package_diagram` in this directory for the visual diagram. Need Auditing

---
## 🧱 Task 1 - Detailed Class Diagram Overview

The Business Logic layer of the HBnB application acts as the internal structure containing core models and rules. To provide a clear representation, this layer defines the behavioral attributes, operational methods, and strict object-oriented relationships governing the key system entities.

---

### 🏛️ Core Entity Definitions

#### 1. Base Model (BaseModel)
- **Responsibility:** Serves as the abstract parent class and foundational blueprint for all application entities.
- **Components:**
  - `id` (Unique identifier generated using UUID4 string format)
  - `created_at` (Timestamp tracking the initialization of the instance)
  - `updated_at` (Timestamp tracking the last data modification)
- **Rule:** This model enforces system-wide consistency, utilizing a `save()` method to update timestamps and a `to_dict()` method for dictionary object serialization.

#### 2. User
- **Responsibility:** Handles human identity credentials, access permissions, and account operations.
- **Components:**
  - Profile details (`first_name`, `last_name`, `email`, `password`)
  - Role management status (`is_admin` boolean flag)
- **Rule:** This entity manages profile states and verification boundaries via `register()`, `login()`, and `update_profile()` methods.

#### 3. Place
- **Responsibility:** Handles property listing registrations, detail management, and hosting parameters.
- **Components:**
  - Listing attributes (`title`, `description`, `price_per_night`, `latitude`, `longitude`)
  - Identity pointers (`owner_id` tracking back to the host, and a list collection of `amenity_ids`)
- **Rule:** This entity updates spatial and cost records through `create_place()`, `update_details()`, `add_amenity()`, and structural `get_reviews()` calls.

#### 4. Review
- **Responsibility:** Handles qualitative ratings, community feedback loops, and guest commentary.
- **Components:**
  - Relational connections (`place_id` targeting the accommodation, and `user_id` targeting the author)
  - Feedback information (`rating` integer value boundaries, and textual `comment`)
- **Rule:** This entity creates and updates transactional user metrics through the `create_review()` and `edit_comment()` methods.

#### 5. Amenity
- **Responsibility:** Handles distinct facility characteristics and features associated with specific listings.
- **Components:**
  - Descriptive features (`name` identifier, and informational `description` outline)
- **Rule:** This entity isolates cataloged property characteristics using the `create_amenity()` routine.

---

### 🔄 Relationship Rules & Structural Logic

The object-oriented design structures how individual elements interact within the layer without exposing persistence or routing components:

- **Generalization (Inheritance):** `User`, `Place`, `Review`, and `Amenity` all inherit from `BaseModel`. This shared architecture ensures every core object automatically possesses tracking mechanisms (`id`, `created_at`, `updated_at`) without duplicating code.
- **Direct Association (Ownership):** A single User can manage or own multiple Places on the platform (a one-to-many relationship), while an individual Place belongs strictly to one designated owner.
- **Composition (Life-cycle Dependency):** A Place serves as a direct container for its Review records. Because a review cannot exist without a property context, its life-cycle is bound directly to the accommodation; deleting a Place listing automatically cascades and removes all associated reviews.
- **Shared Association (Many-to-Many Mapping):** The relationship between a Place and an Amenity is mapped independently. A single Place can link to several Amenities, and a single Amenity can apply to numerous distinct property listings across the system.










## Authors
-Ahaad AL-Qahtani  <Email>
-Areej Al-Ghamdi   <Email>
-Hadeel Al-Qahatni <Email>
