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

@router.get(
    "",
    response_model=list[BIARead],
)
def lister_bias(
    db: Session = Depends(get_db),
):
    return service.lister_bias(db)



@router.get(
    "/{bia_id}",
    response_model=BIARead,
)
def obtenir_bia(
    bia_id: int,
    db: Session = Depends(get_db),
):
    return service.obtenir_bia(db, bia_id)

