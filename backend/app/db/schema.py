from decimal import Decimal
from pydantic import BaseModel, Field, constr, conint, condecimal

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
