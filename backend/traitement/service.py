from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.risques.models import Risque
from backend.traitement.models import Traitement
from backend.traitement.schemas import (
    StatutTraitement,
    TraitementCreate,
    TraitementUpdate,
)


def _obtenir_risque(
    db: Session,
    risque_id: int,
) -> Risque:
    risque = db.get(Risque, risque_id)

    if risque is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risque introuvable.",
        )

    if risque.statut != "valide":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Un traitement ne peut être associé "
                "qu'à un risque validé."
            ),
        )

    return risque


def _est_en_retard(traitement: Traitement) -> bool:
    return (
        traitement.echeance < date.today()
        and traitement.statut
        not in {
            StatutTraitement.TERMINE.value,
            StatutTraitement.ANNULE.value,
        }
    )


def _serialiser(traitement: Traitement) -> dict:
    return {
        "id": traitement.id,
        "risque_id": traitement.risque_id,
        "mesure": traitement.mesure,
        "responsable": traitement.responsable,
        "echeance": traitement.echeance,
        "statut": traitement.statut,
        "description": traitement.description,
        "commentaire": traitement.commentaire,
        "date_realisation": traitement.date_realisation,
        "en_retard": _est_en_retard(traitement),
    }


def creer_traitement(
    db: Session,
    data: TraitementCreate,
) -> dict:
    _obtenir_risque(db, data.risque_id)

    # if data.echeance < date.today():
    #     raise HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         detail="L'échéance ne peut pas être dans le passé.",
    #     )

    traitement = Traitement(
        risque_id=data.risque_id,
        mesure=data.mesure,
        responsable=data.responsable,
        echeance=data.echeance,
        statut=data.statut.value,
        description=data.description,
        commentaire=data.commentaire,
        date_realisation=data.date_realisation,
    )

    db.add(traitement)
    db.commit()
    db.refresh(traitement)

    return _serialiser(traitement)


def lister_traitements(
    db: Session,
    uniquement_en_retard: bool = False,
) -> list[dict]:
    traitements = db.scalars(
        select(Traitement)
        .order_by(Traitement.echeance, Traitement.id)
    ).all()

    resultats = [
        _serialiser(traitement)
        for traitement in traitements
    ]

    if uniquement_en_retard:
        return [
            traitement
            for traitement in resultats
            if traitement["en_retard"]
        ]

    return resultats


def obtenir_traitement(
    db: Session,
    traitement_id: int,
) -> dict:
    traitement = db.get(Traitement, traitement_id)

    if traitement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Traitement introuvable.",
        )

    return _serialiser(traitement)


def modifier_traitement(
    db: Session,
    traitement_id: int,
    data: TraitementUpdate,
) -> dict:
    traitement = db.get(Traitement, traitement_id)

    if traitement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Traitement introuvable.",
        )

    valeurs = data.model_dump(
        exclude_unset=True,
    )

    echeance = valeurs.get(
        "echeance",
        traitement.echeance,
    )

    statut = valeurs.get(
        "statut",
        traitement.statut,
    )

    # if echeance < date.today() and statut not in {
    #     StatutTraitement.TERMINE,
    #     StatutTraitement.ANNULE,
    #     StatutTraitement.TERMINE.value,
    #     StatutTraitement.ANNULE.value,
    # }:
    #     raise HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         detail="L'échéance ne peut pas être dans le passé.",
    #     )

    if statut in {
        StatutTraitement.TERMINE,
        StatutTraitement.TERMINE.value,
    } and valeurs.get(
        "date_realisation",
        traitement.date_realisation,
    ) is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "La date de réalisation est obligatoire "
                "pour un traitement terminé."
            ),
        )

    for nom, valeur in valeurs.items():
        if isinstance(valeur, StatutTraitement):
            valeur = valeur.value

        setattr(traitement, nom, valeur)

    db.commit()
    db.refresh(traitement)

    return _serialiser(traitement)


def supprimer_traitement(
    db: Session,
    traitement_id: int,
) -> None:
    traitement = db.get(Traitement, traitement_id)

    if traitement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Traitement introuvable.",
        )

    db.delete(traitement)
    db.commit()


def obtenir_dashboard_traitements(
    db: Session,
) -> dict:
    traitements = db.scalars(
        select(Traitement)
    ).all()

    serialises = [
        _serialiser(traitement)
        for traitement in traitements
    ]

    return {
        "total": len(serialises),
        "planifies": sum(
            t["statut"] == StatutTraitement.PLANIFIE.value
            for t in serialises
        ),
        "en_cours": sum(
            t["statut"] == StatutTraitement.EN_COURS.value
            for t in serialises
        ),
        "termines": sum(
            t["statut"] == StatutTraitement.TERMINE.value
            for t in serialises
        ),
        "annules": sum(
            t["statut"] == StatutTraitement.ANNULE.value
            for t in serialises
        ),
        "en_retard": sum(
            t["en_retard"]
            for t in serialises
        ),
    }