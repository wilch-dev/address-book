from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from database import get_db, Address as AddressModel
from schemas import Address, AddressCreate, AddressUpdate, AddressDistance
from utils import calculate_distance

# Create FastAPI app
app = FastAPI(
    title="Address Book API",
    description="RESTful API for managing addresses with distance-based retrieval",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Address Book API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.post("/addresses", response_model=Address, tags=["Addresses"])
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address.
    
    - **address**: Full address string (required, must be unique)
    - **latitude**: Latitude coordinate between -90 and 90 (required)
    - **longitude**: Longitude coordinate between -180 and 180 (required)
    """
    db_address = AddressModel(
        address=address.address,
        latitude=address.latitude,
        longitude=address.longitude
    )
    db.add(db_address)
    try:
        db.commit()
        db.refresh(db_address)
        return db_address
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Address '{address.address}' already exists in the database"
        )


@app.get("/addresses", response_model=List[Address], tags=["Addresses"])
def get_all_addresses(db: Session = Depends(get_db)):
    """
    Retrieve all addresses from the database.
    """
    addresses = db.query(AddressModel).all()
    return addresses


@app.get("/addresses/{address_id}", response_model=Address, tags=["Addresses"])
def get_address(address_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific address by ID.
    
    - **address_id**: The ID of the address to retrieve
    """
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.put("/addresses/{address_id}", response_model=Address, tags=["Addresses"])
def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing address.
    
    - **address_id**: The ID of the address to update
    - All fields are optional; only provided fields will be updated
    """
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Update only provided fields
    update_data = address_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_address, field, value)
    
    db.add(db_address)
    try:
        db.commit()
        db.refresh(db_address)
        return db_address
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Address '{update_data.get('address')}' already exists in the database"
        )


@app.delete("/addresses/{address_id}", tags=["Addresses"])
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address by ID.
    
    - **address_id**: The ID of the address to delete
    """
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted successfully", "id": address_id}


@app.get("/addresses/nearby/search", response_model=List[AddressDistance], tags=["Search"])
def get_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude of search center"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude of search center"),
    distance_km: float = Query(10, gt=0, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all addresses within a given distance from specified coordinates.
    
    - **latitude**: Latitude of the search center point (-90 to 90)
    - **longitude**: Longitude of the search center point (-180 to 180)
    - **distance_km**: Search radius in kilometers (default: 10 km)
    
    Returns addresses sorted by distance from the search center.
    """
    all_addresses = db.query(AddressModel).all()
    
    nearby_addresses = []
    for address in all_addresses:
        distance = calculate_distance(
            latitude,
            longitude,
            address.latitude,
            address.longitude
        )
        
        if distance <= distance_km:
            nearby_addresses.append({
                "id": address.id,
                "street": address.street,
                "city": address.city,
                "state": address.state,
                "postal_code": address.postal_code,
                "country": address.country,
                "latitude": address.latitude,
                "longitude": address.longitude,
                "distance": round(distance, 2)
            })
    
    # Sort by distance
    nearby_addresses.sort(key=lambda x: x["distance"])
    
    return nearby_addresses


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
