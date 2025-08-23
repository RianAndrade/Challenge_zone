from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field, constr, conint, condecimal, EmailStr,field_validator


# Validacao do Json


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

# Saída
class PropertyOut(PropertyCreate):
    id: int

    class Config:
        from_attributes = True  



class ReservationCreate(BaseModel):
    property_id: int = Field(..., description="ID da propriedade")
    client_name: str = Field(..., min_length=1, max_length=255)
    client_email: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: date
    guests_quantity: conint(ge=1) 

    # end_date > start_date

    @field_validator("end_date")
    @classmethod
    def check_dates(cls, v: date, info):
        start = info.data.get("start_date")
        if start is not None and v <= start:
            raise ValueError("end_date tem que ser maior que start_date")
        return v

class ReservationOut(ReservationCreate):
    id: int

    class Config:
        from_attributes = True 


class ReservationCreateResponse(BaseModel):
    message: str
    reservation: ReservationOut

    class Config:
        from_attributes = True