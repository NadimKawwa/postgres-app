from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict

class Address(BaseModel):
    street: str
    city: str
    zip: str

class RestaurantCreate(BaseModel):
    name: str = Field(..., min_length=1)
    address: Address
    cuisine: str
    hours: Dict[str, str]
    rating: float = Field(..., ge=0, le=5)
    review_count: int = Field(0, ge=0)
    description: str

    @field_validator('hours')
    @classmethod
    def validate_hours(cls, v):
        valid_days = {'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'}
        if not all(day in valid_days for day in v.keys()):
            raise ValueError("Hours must contain keys for days of the week (mon-sun)")
        return v

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[Address] = None
    cuisine: Optional[str] = None
    hours: Optional[Dict[str, str]] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    description: Optional[str] = None