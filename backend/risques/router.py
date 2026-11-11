from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.risques import service
from backend.risques.schemas import (
    RisqueCreate,
    RisqueRead,
    RisqueUpdate,
)

router = APIRouter(
    prefix="/risques",
    tags=["Risques"],
)


@router.post(
    "",
    response_model=RisqueRead,
    status_code=status.HTTP_201_CREATED,
)
def creer_risque(
    data: RisqueCreate,
    db: Session = Depends(get_db),
):
    return service.creer_risque(
        db,
        data,
    )


@router.get(
    "",
    response_model=list[RisqueRead],
)
def lister_risques(
    db: Session = Depends(get_db),
):
    return service.lister_risques(db)


@router.get(
    "/{risque_id}",
    response_model=RisqueRead,
)
def obtenir_risque(
    risque_id: int,
    db: Session = Depends(get_db),
):
    return service.obtenir_risque(
        db,
        risque_id,
    )


@router.put(
    "/{risque_id}",
    response_model=RisqueRead,
)
def modifier_risque(
    risque_id: int,
    data: RisqueUpdate,
    db: Session = Depends(get_db),
):
    return service.modifier_risque(
        db,
        risque_id,
        data,
    )


@router.post(
    "/{risque_id}/soumettre",
    response_model=RisqueRead,
)
def soumettre_risque(
    risque_id: int,
    db: Session = Depends(get_db),
):
    return service.soumettre_risque(
        db,
        risque_id,
    )


@router.post(
    "/{risque_id}/valider",
    response_model=RisqueRead,
)
def valider_risque(
    risque_id: int,
    db: Session = Depends(get_db),
):
    return service.valider_risque(
        db,
        risque_id,
    )


@router.post(
    "/{risque_id}/a-corriger",
    response_model=RisqueRead,
)
def corriger_risque(
    risque_id: int,
    db: Session = Depends(get_db),
):
    return service.corriger_risque(
        db,
        risque_id,
    )