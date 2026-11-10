from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.cartographie import service
from backend.cartographie.schemas import (
    CartographieRead,
    StatistiquesCartographieRead,
)
from backend.core.database import get_db


router = APIRouter(
    prefix="/cartographie",
    tags=["Cartographie"],
)


@router.get(
    "",
    response_model=CartographieRead,
)
def obtenir_cartographie(
    db: Session = Depends(get_db),
):
    return service.obtenir_heatmap(db)


@router.get(
    "/heatmap",
    response_model=CartographieRead,
)
def obtenir_heatmap(
    db: Session = Depends(get_db),
):
    return service.obtenir_heatmap(db)


@router.get(
    "/statistiques",
    response_model=StatistiquesCartographieRead,
)
def obtenir_statistiques(
    db: Session = Depends(get_db),
):
    return service.obtenir_statistiques(db)