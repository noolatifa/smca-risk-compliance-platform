from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.referentiel.models import Activite, Dependance, Ressource
from backend.referentiel.schemas import (
    ActiviteCreate,
    DependanceCreate,
    RessourceCreate,
)


# --- Outils communs (évitent de dupliquer le code Activité / Ressource) ------

def _obtenir(db: Session, modele, identifiant: int, libelle: str):
    objet = db.get(modele, identifiant)

    if objet is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{libelle} introuvable.")

    return objet


def _lister(db: Session, modele, inclure_archives: bool):
    requete = select(modele).order_by(modele.nom)

    if not inclure_archives:
        requete = requete.where(modele.archive.is_(False))

    return list(db.scalars(requete))


def _enregistrer(db: Session, objet):
    db.add(objet)
    db.commit()
    db.refresh(objet)

    return objet


# --- Activités ---------------------------------------------------------------

def creer_activite(db: Session, data: ActiviteCreate) -> Activite:
    return _enregistrer(db, Activite(**data.model_dump()))


def lister_activites(db: Session, inclure_archives: bool = False) -> list[Activite]:
    return _lister(db, Activite, inclure_archives)


def obtenir_activite(db: Session, activite_id: int) -> Activite:
    return _obtenir(db, Activite, activite_id, "Activité")


def archiver_activite(db: Session, activite_id: int) -> Activite:
    activite = obtenir_activite(db, activite_id)
    activite.archive = True

    return _enregistrer(db, activite)


# --- Ressources --------------------------------------------------------------

def creer_ressource(db: Session, data: RessourceCreate) -> Ressource:
    return _enregistrer(db, Ressource(**data.model_dump()))


def lister_ressources(db: Session, inclure_archives: bool = False) -> list[Ressource]:
    return _lister(db, Ressource, inclure_archives)


def obtenir_ressource(db: Session, ressource_id: int) -> Ressource:
    return _obtenir(db, Ressource, ressource_id, "Ressource")


def archiver_ressource(db: Session, ressource_id: int) -> Ressource:
    ressource = obtenir_ressource(db, ressource_id)
    ressource.archive = True

    return _enregistrer(db, ressource)


# --- Dépendances -------------------------------------------------------------

def creer_dependance(db: Session, data: DependanceCreate) -> Dependance:
    activite = obtenir_activite(db, data.activite_id)
    ressource = obtenir_ressource(db, data.ressource_id)

    if activite.archive or ressource.archive:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Impossible de créer une dépendance avec un élément archivé.",
        )

    deja_lie = db.scalar(
        select(Dependance.id).where(
            Dependance.activite_id == data.activite_id,
            Dependance.ressource_id == data.ressource_id,
        )
    )

    if deja_lie is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Cette dépendance existe déjà.")

    return _enregistrer(db, Dependance(**data.model_dump()))


def lister_dependances(
    db: Session,
    activite_id: int | None = None,
    ressource_id: int | None = None,
) -> list[Dependance]:
    requete = select(Dependance).order_by(Dependance.id)

    if activite_id is not None:
        requete = requete.where(Dependance.activite_id == activite_id)

    if ressource_id is not None:
        requete = requete.where(Dependance.ressource_id == ressource_id)

    return list(db.scalars(requete))
