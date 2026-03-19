# Address Book API - Bruno Collection

This is a Bruno API collection for testing the Address Book API endpoints.

## How to Import into Bruno

1. Open Bruno
2. Click on "Collections" in the left sidebar
3. Click the "+" button or "Import Collection"
4. Select the `collection` folder from this project
5. Bruno will automatically load all `.yml` request files

All requests are defined as individual `.yml` files that Bruno will recognize and import.

## Collection Contents

The collection includes the following endpoints:

### CRUD Operations
- **Create Address** - POST `/addresses` - Create a new address
- **Get All Addresses** - GET `/addresses` - Retrieve all addresses
- **Get Single Address** - GET `/addresses/1` - Get a specific address by ID
- **Update Address** - PUT `/addresses/1` - Update an address
- **Delete Address** - DELETE `/addresses/1` - Delete an address

### Distance-Based Search
- **Search Nearby Addresses - 50km NYC** - GET `/addresses/nearby/search?latitude=40.7128&longitude=-74.0060&distance_km=50`
- **Search Nearby Addresses - 10km LA** - GET `/addresses/nearby/search?latitude=34.0522&longitude=-118.2437&distance_km=10`

## Prerequisites

Make sure the FastAPI server is running before testing:

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`

## Testing Workflow

1. **Create Addresses** - Use the "Create Address" request to add test data
2. **Get All Addresses** - Verify addresses were created
3. **Search Nearby** - Test the distance-based search functionality
4. **Update Address** - Modify an existing address
5. **Delete Address** - Remove an address

## Notes

- All requests use `http://localhost:8000` as the base URL
- The "Create Address" request includes sample data for New York
- Modify the address ID in "Get Single Address", "Update Address", and "Delete Address" requests as needed
- The search endpoints use real coordinates for NYC and LA
