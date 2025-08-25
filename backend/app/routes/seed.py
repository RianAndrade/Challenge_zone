from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.service.seeds import apply_full_seed

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("", status_code=status.HTTP_201_CREATED)
def run_seed(db: Session = Depends(get_db)):
    try:
        result = apply_full_seed(db)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao semear: {e}")
