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


def list_properties(db: Session) -> list[Property]:
    return db.query(Property).order_by(Property.id.asc()).all()


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
