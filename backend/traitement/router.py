from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.traitement import service
from backend.traitement.schemas import (
    TraitementCreate,
    TraitementDashboardRead,
    TraitementRead,
    TraitementUpdate,
)

router = APIRouter(
    prefix="/traitements",
    tags=["Traitements"],
)


@router.post(
    "",
    response_model=TraitementRead,
    status_code=status.HTTP_201_CREATED,
)
def creer_traitement(
    data: TraitementCreate,
    db: Session = Depends(get_db),
):
    return service.creer_traitement(db, data)


@router.get(
    "",
    response_model=list[TraitementRead],
)
def lister_traitements(
    uniquement_en_retard: bool = False,
    db: Session = Depends(get_db),
):
    return service.lister_traitements(
        db,
        uniquement_en_retard,
    )


@router.get(
    "/dashboard",
    response_model=TraitementDashboardRead,
)
def dashboard_traitements(
    db: Session = Depends(get_db),
):
    return service.obtenir_dashboard_traitements(db)


@router.get(
    "/{traitement_id}",
    response_model=TraitementRead,
)
def obtenir_traitement(
    traitement_id: int,
    db: Session = Depends(get_db),
):
    return service.obtenir_traitement(db, traitement_id)


@router.put(
    "/{traitement_id}",
    response_model=TraitementRead,
)
def modifier_traitement(
    traitement_id: int,
    data: TraitementUpdate,
    db: Session = Depends(get_db),
):
    return service.modifier_traitement(
        db,
        traitement_id,
        data,
    )


@router.delete(
    "/{traitement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def supprimer_traitement(
    traitement_id: int,
    db: Session = Depends(get_db),
):
    service.supprimer_traitement(db, traitement_id)