from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.referentiel.models import Activite, Ressource
from backend.risques.models import Risque
from backend.risques.schemas import RisqueCreate, RisqueUpdate


def calculer_niveau(score: int) -> str:
    if score <= 3:
        return "faible"

    if score <= 8:
        return "modere"

    return "eleve"


def _obtenir_activites(
    db: Session,
    ids: list[int],
) -> list[Activite]:
    ids_uniques = set(ids)

    activites = list(
        db.scalars(
            select(Activite).where(Activite.id.in_(ids_uniques))
        ).all()
    )

    if len(activites) != len(ids_uniques):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Une ou plusieurs activités sont introuvables.",
        )

    return activites


def _obtenir_ressources(
    db: Session,
    ids: list[int],
) -> list[Ressource]:
    if not ids:
        return []

    ids_uniques = set(ids)

    ressources = list(
        db.scalars(
            select(Ressource).where(Ressource.id.in_(ids_uniques))
        ).all()
    )

    if len(ressources) != len(ids_uniques):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Une ou plusieurs ressources sont introuvables.",
        )

    return ressources


def _serialiser(risque: Risque) -> dict:
    return {
        "id": risque.id,
        "scenario": risque.scenario,
        "cause": risque.cause,
        "menace": risque.menace,
        "vulnerabilite": risque.vulnerabilite,
        "consequences": risque.consequences,
        "proprietaire": risque.proprietaire,
        "activite_ids": [
            activite.id
            for activite in risque.activites
        ],
        "ressource_ids": [
            ressource.id
            for ressource in risque.ressources
        ],
        "probabilite": risque.probabilite,
        "impact": risque.impact,
        "score_criticite": risque.score_criticite,
        "niveau": risque.niveau,
        "statut": risque.statut,
    }


def _obtenir_risque_objet(
    db: Session,
    risque_id: int,
) -> Risque:
    risque = db.get(Risque, risque_id)

    if risque is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risque introuvable.",
        )

    return risque


def creer_risque(
    db: Session,
    data: RisqueCreate,
) -> dict:
    activites = _obtenir_activites(
        db,
        data.activite_ids,
    )

    ressources = _obtenir_ressources(
        db,
        data.ressource_ids,
    )

    score = data.probabilite * data.impact

    risque = Risque(
        scenario=data.scenario,
        cause=data.cause,
        menace=data.menace,
        vulnerabilite=data.vulnerabilite,
        consequences=data.consequences,
        proprietaire=data.proprietaire,
        probabilite=data.probabilite,
        impact=data.impact,
        score_criticite=score,
        niveau=calculer_niveau(score),
        statut=data.statut.value,
        activites=activites,
        ressources=ressources,
    )

    db.add(risque)
    db.commit()
    db.refresh(risque)

    return _serialiser(risque)


def lister_risques(
    db: Session,
) -> list[dict]:
    risques = db.scalars(
        select(Risque).order_by(Risque.id)
    ).all()

    return [
        _serialiser(risque)
        for risque in risques
    ]


def obtenir_risque(
    db: Session,
    risque_id: int,
) -> dict:
    risque = _obtenir_risque_objet(
        db,
        risque_id,
    )

    return _serialiser(risque)


def modifier_risque(
    db: Session,
    risque_id: int,
    data: RisqueUpdate,
) -> dict:
    risque = _obtenir_risque_objet(
        db,
        risque_id,
    )

    valeurs = data.model_dump(
        exclude_unset=True,
        exclude={
            "activite_ids",
            "ressource_ids",
        },
    )

    probabilite = valeurs.get(
        "probabilite",
        risque.probabilite,
    )

    impact = valeurs.get(
        "impact",
        risque.impact,
    )

    for nom, valeur in valeurs.items():
        setattr(risque, nom, valeur)

    risque.probabilite = probabilite
    risque.impact = impact
    risque.score_criticite = probabilite * impact
    risque.niveau = calculer_niveau(
        risque.score_criticite,
    )

    if data.activite_ids is not None:
        risque.activites = _obtenir_activites(
            db,
            data.activite_ids,
        )

    if data.ressource_ids is not None:
        risque.ressources = _obtenir_ressources(
            db,
            data.ressource_ids,
        )

    db.commit()
    db.refresh(risque)

    return _serialiser(risque)


def soumettre_risque(
    db: Session,
    risque_id: int,
) -> dict:
    risque = _obtenir_risque_objet(
        db,
        risque_id,
    )

    if risque.statut not in {
        "brouillon",
        "a_corriger",
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce risque ne peut pas être soumis.",
        )

    risque.statut = "soumis"

    db.commit()
    db.refresh(risque)

    return _serialiser(risque)


def valider_risque(
    db: Session,
    risque_id: int,
) -> dict:
    risque = _obtenir_risque_objet(
        db,
        risque_id,
    )

    if risque.statut != "soumis":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seul un risque soumis peut être validé.",
        )

    risque.statut = "valide"

    db.commit()
    db.refresh(risque)

    return _serialiser(risque)


def corriger_risque(
    db: Session,
    risque_id: int,
) -> dict:
    risque = _obtenir_risque_objet(
        db,
        risque_id,
    )

    if risque.statut != "soumis":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seul un risque soumis peut être renvoyé en correction.",
        )

    risque.statut = "a_corriger"

    db.commit()
    db.refresh(risque)

    return _serialiser(risque)