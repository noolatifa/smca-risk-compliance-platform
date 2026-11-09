from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.bia import service
from backend.bia.schemas import BIACreate, BIARead
from backend.core.database import get_db


router = APIRouter(
    prefix="/bia",
    tags=["BIA"],
)


@router.post(
    "",
    response_model=BIARead,
    status_code=status.HTTP_201_CREATED,
)
def creer_bia(
    data: BIACreate,
    db: Session = Depends(get_db),
):
    return service.creer_bia(db, data)