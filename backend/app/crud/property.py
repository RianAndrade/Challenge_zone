from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, func

from app.db.models import Property
from app.db.schema import PropertyCreate

def create_property(db: Session, data: PropertyCreate) -> Property:
    obj = Property(**data.model_dump())
    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Já existe uma propriedade cadastrada nesse endereço.") from e
    db.refresh(obj)
    return obj


def list_properties(
    db: Session,
    location: Optional[str] = None,
    capacity: Optional[int] = None,
    address_neighborhood: Optional[str] = None,
    address_city: Optional[str] = None,
    address_state: Optional[str] = None,
    price_per_night: Optional[int] = None 
) -> List[Property]:

    q = db.query(Property)

    if address_state: 
        q = q.filter(func.lower(Property.address_state).like(f"%{address_state.lower()}%"))
    
    if address_neighborhood:
        q = q.filter(func.lower(Property.address_neighborhood).like(f"%{address_neighborhood.lower()}%"))

    if address_city:
        q = q.filter(func.lower(Property.address_city).like(f"%{address_city.lower()}%"))

#esta maior ou igual para facilitar debug mudar para enviar

    if capacity:
        q = q.filter(Property.capacity >= capacity)

    if price_per_night:
        q = q.filter(Property.price_per_night <= price_per_night)

    return q.order_by(asc(Property.id)).all()


def delete_property_by_id(db: Session, prop_id: int) -> bool:
    obj = db.get(Property, prop_id)
    if not obj:
        return False
    db.delete(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # se houver restrições de FK sem CASCADE
        raise ValueError("Cannot delete property due to related records.") from e
    return True
