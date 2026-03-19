"""
Test script for the Address Book API
Run this after starting the FastAPI server with: python main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_create_addresses():
    """Test creating addresses"""
    addresses = [
        {
            "address": "123 Main St, New York, NY 10001, USA",
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        {
            "address": "456 Park Ave, New York, NY 10022, USA",
            "latitude": 40.7614,
            "longitude": -73.9776
        },
        {
            "address": "789 Broadway, New York, NY 10003, USA",
            "latitude": 40.7505,
            "longitude": -73.9972
        },
        {
            "address": "321 5th Ave, Los Angeles, CA 90001, USA",
            "latitude": 34.0522,
            "longitude": -118.2437
        }
    ]
    
    created_ids = []
    for addr in addresses:
        response = requests.post(f"{BASE_URL}/addresses", json=addr)
        print_response(f"Create Address: {addr['street']}", response)
        if response.status_code == 200:
            created_ids.append(response.json()["id"])
    
    return created_ids


def test_get_all_addresses():
    """Test retrieving all addresses"""
    response = requests.get(f"{BASE_URL}/addresses")
    print_response("Get All Addresses", response)


def test_get_single_address(address_id):
    """Test retrieving a single address"""
    response = requests.get(f"{BASE_URL}/addresses/{address_id}")
    print_response(f"Get Address ID {address_id}", response)


def test_update_address(address_id):
    """Test updating an address"""
    update_data = {
        "address": "999 Updated St, New York, NY 10099, USA"
    }
    response = requests.put(f"{BASE_URL}/addresses/{address_id}", json=update_data)
    print_response(f"Update Address ID {address_id}", response)


def test_nearby_addresses():
    """Test retrieving nearby addresses"""
    # Search near New York (40.7128, -74.0060) within 50 km
    response = requests.get(
        f"{BASE_URL}/addresses/nearby/search",
        params={
            "latitude": 40.7128,
            "longitude": -74.0060,
            "distance_km": 50
        }
    )
    print_response("Get Nearby Addresses (50 km from NYC)", response)
    
    # Search near Los Angeles (34.0522, -118.2437) within 10 km
    response = requests.get(
        f"{BASE_URL}/addresses/nearby/search",
        params={
            "latitude": 34.0522,
            "longitude": -118.2437,
            "distance_km": 10
        }
    )
    print_response("Get Nearby Addresses (10 km from LA)", response)


def test_delete_address(address_id):
    """Test deleting an address"""
    response = requests.delete(f"{BASE_URL}/addresses/{address_id}")
    print_response(f"Delete Address ID {address_id}", response)


def test_validation_errors():
    """Test validation errors"""
    # Invalid latitude
    invalid_addr = {
        "address": "123 Test St, Test City, TS 12345, Test Country",
        "latitude": 95,  # Invalid: > 90
        "longitude": -74.0060
    }
    response = requests.post(f"{BASE_URL}/addresses", json=invalid_addr)
    print_response("Validation Error: Invalid Latitude", response)
    
    # Invalid longitude
    invalid_addr = {
        "address": "123 Test St, Test City, TS 12345, Test Country",
        "latitude": 40.7128,
        "longitude": 200  # Invalid: > 180
    }
    response = requests.post(f"{BASE_URL}/addresses", json=invalid_addr)
    print_response("Validation Error: Invalid Longitude", response)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("ADDRESS BOOK API TEST SUITE")
    print("="*60)
    
    try:
        # Test creating addresses
        print("\n[1] Testing Address Creation...")
        created_ids = test_create_addresses()
        
        # Test getting all addresses
        print("\n[2] Testing Get All Addresses...")
        test_get_all_addresses()
        
        # Test getting single address
        if created_ids:
            print("\n[3] Testing Get Single Address...")
            test_get_single_address(created_ids[0])
        
        # Test updating address
        if created_ids:
            print("\n[4] Testing Update Address...")
            test_update_address(created_ids[0])
        
        # Test nearby addresses
        print("\n[5] Testing Nearby Addresses Search...")
        test_nearby_addresses()
        
        # Test validation errors
        print("\n[6] Testing Validation Errors...")
        test_validation_errors()
        
        # Test deleting address
        if created_ids:
            print("\n[7] Testing Delete Address...")
            test_delete_address(created_ids[-1])
        
        print("\n" + "="*60)
        print("TEST SUITE COMPLETED")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Make sure the FastAPI server is running with: python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
