from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field, constr, conint, condecimal, EmailStr, field_validator
from pydantic import ConfigDict 

class PropertyCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=160)
    address_street: constr(strip_whitespace=True, min_length=1, max_length=160)
    address_number: constr(strip_whitespace=True, min_length=1, max_length=32)
    address_neighborhood: constr(strip_whitespace=True, min_length=1, max_length=120)
    address_city: constr(strip_whitespace=True, min_length=1, max_length=120)
    address_state: constr(strip_whitespace=True, min_length=2, max_length=8)
    country: constr(strip_whitespace=True, min_length=3, max_length=3) = "BRA"
    rooms: conint(ge=0)
    capacity: conint(ge=0)
    price_per_night: condecimal(max_digits=10, decimal_places=2, ge=Decimal("0"))

class PropertyOut(PropertyCreate):
    model_config = ConfigDict(from_attributes=True) 
    id: int


class ReservationCreate(BaseModel):
    model_config = ConfigDict(extra='forbid') 
    property_id: int = Field(..., description="ID da propriedade")
    client_name: str = Field(..., min_length=1, max_length=255)
    client_email: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: date
    guests_quantity: conint(ge=0)


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')
    id: int
    property_id: int
    client_name: str
    client_email: str
    start_date: date
    end_date: date
    guests_quantity: int
    is_active: bool  # aparece só na resposta

class ReservationCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')
    message: str
    reservation: ReservationOut