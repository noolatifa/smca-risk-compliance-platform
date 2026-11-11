from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.referentiel import service
from backend.referentiel.schemas import (
    ActiviteCreate,
    ActiviteRead,
    DependanceCreate,
    DependanceRead,
    RessourceCreate,
    RessourceRead,
)

router = APIRouter()

activites = APIRouter(prefix="/activites", tags=["Activités"])
ressources = APIRouter(prefix="/ressources", tags=["Ressources"])
dependances = APIRouter(prefix="/dependances", tags=["Dépendances"])


# --- Activités ---------------------------------------------------------------

@activites.post("", response_model=ActiviteRead, status_code=status.HTTP_201_CREATED)
def creer_activite(data: ActiviteCreate, db: Session = Depends(get_db)):
    return service.creer_activite(db, data)


@activites.get("", response_model=list[ActiviteRead])
def lister_activites(inclure_archives: bool = False, db: Session = Depends(get_db)):
    return service.lister_activites(db, inclure_archives)


@activites.get("/{activite_id}", response_model=ActiviteRead)
def obtenir_activite(activite_id: int, db: Session = Depends(get_db)):
    return service.obtenir_activite(db, activite_id)


@activites.post("/{activite_id}/archiver", response_model=ActiviteRead)
def archiver_activite(activite_id: int, db: Session = Depends(get_db)):
    return service.archiver_activite(db, activite_id)


# --- Ressources --------------------------------------------------------------

@ressources.post("", response_model=RessourceRead, status_code=status.HTTP_201_CREATED)
def creer_ressource(data: RessourceCreate, db: Session = Depends(get_db)):
    return service.creer_ressource(db, data)


@ressources.get("", response_model=list[RessourceRead])
def lister_ressources(inclure_archives: bool = False, db: Session = Depends(get_db)):
    return service.lister_ressources(db, inclure_archives)


@ressources.get("/{ressource_id}", response_model=RessourceRead)
def obtenir_ressource(ressource_id: int, db: Session = Depends(get_db)):
    return service.obtenir_ressource(db, ressource_id)


@ressources.post("/{ressource_id}/archiver", response_model=RessourceRead)
def archiver_ressource(ressource_id: int, db: Session = Depends(get_db)):
    return service.archiver_ressource(db, ressource_id)


# --- Dépendances -------------------------------------------------------------

@dependances.post("", response_model=DependanceRead, status_code=status.HTTP_201_CREATED)
def creer_dependance(data: DependanceCreate, db: Session = Depends(get_db)):
    return service.creer_dependance(db, data)


@dependances.get("", response_model=list[DependanceRead])
def lister_dependances(
    activite_id: int | None = None,
    ressource_id: int | None = None,
    db: Session = Depends(get_db),
):
    return service.lister_dependances(db, activite_id, ressource_id)


router.include_router(activites)
router.include_router(ressources)
router.include_router(dependances)
