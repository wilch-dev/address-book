# Address Book API

A RESTful API built with FastAPI for managing addresses with distance-based retrieval capabilities. Addresses are stored in an SQLite database with full validation.

## Features

- ✅ **Create** new addresses with validation
- ✅ **Read** all addresses or retrieve specific addresses by ID
- ✅ **Update** existing addresses (partial updates supported)
- ✅ **Delete** addresses
- ✅ **Distance-based Search** - Find addresses within a specified distance from coordinates
- ✅ **Coordinate Validation** - Latitude (-90 to 90) and Longitude (-180 to 180)
- ✅ **SQLite Database** - Persistent storage
- ✅ **Interactive API Documentation** - Swagger UI and ReDoc

## Project Structure

```
address-book/
├── main.py              # FastAPI application with all endpoints
├── database.py          # SQLAlchemy models and database configuration
├── schemas.py           # Pydantic models for validation
├── utils.py             # Utility functions (distance calculation)
├── test_api.py          # Test script for API endpoints
├── requirements.txt     # Python dependencies
└── README_API.md        # This file
```

## Installation

### Prerequisites

Make sure you have `uv` installed. If not, install it from [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

### Install Dependencies

```bash
uv sync
```

This will create a virtual environment and install all dependencies from `pyproject.toml`.

## Running the Application

### Start the FastAPI Server

```bash
uv run python main.py
```

Or if you prefer using uvicorn directly:

```bash
uv run uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Address

**POST** `/addresses`

Create a new address in the database.

**Request Body:**
```json
{
  "address": "123 Main St, New York, NY 10001, USA",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Response (201):**
```json
{
  "id": 1,
  "address": "123 Main St, New York, NY 10001, USA",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### 2. Get All Addresses

**GET** `/addresses`

Retrieve all addresses from the database.

**Response:**
```json
[
  {
    "id": 1,
    "address": "123 Main St, New York, NY 10001, USA",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  ...
]
```

### 3. Get Single Address

**GET** `/addresses/{address_id}`

Retrieve a specific address by ID.

**Parameters:**
- `address_id` (path): The ID of the address

**Response:**
```json
{
  "id": 1,
  "address": "123 Main St, New York, NY 10001, USA",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### 4. Update Address

**PUT** `/addresses/{address_id}`

Update an existing address. All fields are optional.

**Parameters:**
- `address_id` (path): The ID of the address to update

**Request Body (all fields optional):**
```json
{
  "address": "456 New St, New York, NY 10002, USA"
}
```

**Response:**
```json
{
  "id": 1,
  "address": "456 New St, New York, NY 10002, USA",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### 5. Delete Address

**DELETE** `/addresses/{address_id}`

Delete an address from the database.

**Parameters:**
- `address_id` (path): The ID of the address to delete

**Response:**
```json
{
  "message": "Address deleted successfully",
  "id": 1
}
```

### 6. Search Nearby Addresses

**GET** `/addresses/nearby/search`

Find all addresses within a specified distance from given coordinates.

**Query Parameters:**
- `latitude` (required): Latitude of search center (-90 to 90)
- `longitude` (required): Longitude of search center (-180 to 180)
- `distance_km` (optional): Search radius in kilometers (default: 10)

**Example:**
```
GET /addresses/nearby/search?latitude=40.7128&longitude=-74.0060&distance_km=50
```

**Response:**
```json
[
  {
    "id": 1,
    "address": "123 Main St, New York, NY 10001, USA",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "distance": 0.0
  },
  {
    "id": 2,
    "address": "456 Park Ave, New York, NY 10022, USA",
    "latitude": 40.7614,
    "longitude": -73.9776,
    "distance": 5.42
  }
]
```

## Validation Rules

### Address Fields

- **address**: Required, 1-500 characters (full address string, must be unique)
- **latitude**: Required, must be between -90 and 90
- **longitude**: Required, must be between -180 and 180

### Uniqueness Constraint

- **address** field must be unique - attempting to create or update an address with a duplicate address string will result in a 400 Bad Request error

### Error Responses

**400 Bad Request** - Validation error:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "latitude"],
      "msg": "ensure this value is less than or equal to 90",
      "input": 95
    }
  ]
}
```

**400 Bad Request** - Duplicate address:
```json
{
  "detail": "Address '123 Main St, New York, NY 10001, USA' already exists in the database"
}
```

**404 Not Found** - Address not found:
```json
{
  "detail": "Address not found"
}
```

## Testing

Run the test script to verify all API endpoints:

```bash
# Terminal 1: Start the server
uv run python main.py

# Terminal 2: Run tests
uv run python test_api.py
```

The test script will:
1. Create multiple addresses
2. Retrieve all addresses
3. Get a single address
4. Update an address
5. Search for nearby addresses
6. Test validation errors
7. Delete an address

## Distance Calculation

The API uses the **Haversine formula** to calculate great-circle distances between coordinates on Earth. This provides accurate distances in kilometers for geographic locations.

### Formula
```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × asin(√a)
d = R × c
```

Where:
- R = Earth's radius (6,371 km)
- lat/lon are in radians

## Database

The application uses **SQLite** for data persistence. The database file (`address_book.db`) is automatically created in the project directory on first run.

### Database Schema

```sql
CREATE TABLE addresses (
    id INTEGER PRIMARY KEY,
    address VARCHAR,
    latitude FLOAT,
    longitude FLOAT
);
```

## Example Usage with cURL

### Create an address
```bash
curl -X POST "http://localhost:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Main St, New York, NY 10001, USA",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

### Get all addresses
```bash
curl "http://localhost:8000/addresses"
```

### Search nearby addresses
```bash
curl "http://localhost:8000/addresses/nearby/search?latitude=40.7128&longitude=-74.0060&distance_km=50"
```

### Update an address
```bash
curl -X PUT "http://localhost:8000/addresses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "456 New St, New York, NY 10002, USA"
  }'
```

### Delete an address
```bash
curl -X DELETE "http://localhost:8000/addresses/1"
```

## Dependencies

All dependencies are managed in [`pyproject.toml`](pyproject.toml) and installed via `uv`:

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **Requests** - HTTP client library (for testing)

Install all dependencies with:
```bash
uv sync
```

## License

MIT License
