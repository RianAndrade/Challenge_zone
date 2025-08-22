from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Property
from app.schema import PropertyCreate

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
