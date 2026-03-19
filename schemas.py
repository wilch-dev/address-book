from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AddressBase(BaseModel):
    """Base address schema with validation"""
    address: str = Field(..., min_length=1, max_length=500, description="Full address")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")

    @field_validator('latitude', 'longitude')
    @classmethod
    def validate_coordinates(cls, v):
        """Validate that coordinates are valid numbers"""
        if not isinstance(v, (int, float)):
            raise ValueError('Coordinates must be numeric')
        return float(v)


class AddressCreate(AddressBase):
    """Schema for creating a new address"""
    pass


class AddressUpdate(BaseModel):
    """Schema for updating an address"""
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    @field_validator('latitude', 'longitude')
    @classmethod
    def validate_coordinates(cls, v):
        """Validate that coordinates are valid numbers"""
        if v is not None and not isinstance(v, (int, float)):
            raise ValueError('Coordinates must be numeric')
        return float(v) if v is not None else None


class Address(AddressBase):
    """Schema for address response"""
    id: int

    class Config:
        from_attributes = True


class AddressDistance(Address):
    """Schema for address response with distance"""
    distance: float = Field(..., description="Distance in kilometers")

    class Config:
        from_attributes = True
