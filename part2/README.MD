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

## Authors:
- Areej Al-Ghamdi
