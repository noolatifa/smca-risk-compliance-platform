from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.risques.models import Risque


def calculer_niveau(score: int) -> str:
    if score <= 7:
        return "faible"

    if score <= 14:
        return "modere"

    return "eleve"


def obtenir_risques_valides(
    db: Session,
) -> list[Risque]:
    return list(
        db.scalars(
            select(Risque)
            .where(Risque.statut == "valide")
            .order_by(
                Risque.score_criticite.desc(),
                Risque.id,
            )
        ).all()
    )


def serialiser_risque(
    risque: Risque,
) -> dict:
    niveau = calculer_niveau(
        risque.probabilite * risque.impact
    )

    return {
        "id": risque.id,
        "scenario": risque.scenario,
        "probabilite": risque.probabilite,
        "impact": risque.impact,
        "score_criticite": (
            risque.probabilite * risque.impact
        ),
        "niveau": niveau,
        "proprietaire": risque.proprietaire,
        "statut": risque.statut,
    }


def obtenir_heatmap(
    db: Session,
) -> dict:
    risques = obtenir_risques_valides(db)

    matrice = []

    for probabilite in range(1, 6):
        for impact in range(1, 6):
            score = probabilite * impact
            risques_case = [
                risque
                for risque in risques
                if risque.probabilite == probabilite
                and risque.impact == impact
            ]

            matrice.append(
                {
                    "probabilite": probabilite,
                    "impact": impact,
                    "score": score,
                    "niveau": calculer_niveau(score),
                    "nombre_risques": len(risques_case),
                    "risques_ids": [
                        risque.id
                        for risque in risques_case
                    ],
                }
            )

    risques_serialises = [
        serialiser_risque(risque)
        for risque in risques
    ]

    return {
        "matrice": matrice,
        "risques": risques_serialises,
        "total_risques": len(risques),
        "risques_faibles": sum(
            calculer_niveau(
                risque.probabilite * risque.impact
            ) == "faible"
            for risque in risques
        ),
        "risques_moderees": sum(
            calculer_niveau(
                risque.probabilite * risque.impact
            ) == "modere"
            for risque in risques
        ),
        "risques_eleves": sum(
            calculer_niveau(
                risque.probabilite * risque.impact
            ) == "eleve"
            for risque in risques
        ),
    }


def obtenir_statistiques(
    db: Session,
) -> dict:
    risques = obtenir_risques_valides(db)

    risques_serialises = [
        serialiser_risque(risque)
        for risque in risques
    ]

    return {
        "total_risques": len(risques),
        "risques_faibles": sum(
            risque["niveau"] == "faible"
            for risque in risques_serialises
        ),
        "risques_moderees": sum(
            risque["niveau"] == "modere"
            for risque in risques_serialises
        ),
        "risques_eleves": sum(
            risque["niveau"] == "eleve"
            for risque in risques_serialises
        ),
        "top_risques": risques_serialises[:3],
    }