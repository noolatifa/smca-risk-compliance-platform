from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.risques.models import Risque
from backend.traitement.models import Traitement


def calculer_niveau(score: int) -> str:
    if score <= 7:
        return "faible"

    if score <= 14:
        return "modere"

    return "eleve"


def traitement_en_retard(traitement: Traitement) -> bool:
    return (
        traitement.echeance < date.today()
        and traitement.statut not in {
            "termine",
            "annule",
        }
    )


def obtenir_dashboard(db: Session) -> dict:
    risques = list(
        db.scalars(
            select(Risque)
            .where(Risque.statut == "valide")
            .order_by(
                Risque.score_criticite.desc(),
                Risque.id,
            )
        ).all()
    )

    traitements = list(
        db.scalars(
            select(Traitement)
        ).all()
    )

    risques_serialises = []

    for risque in risques:
        score = risque.probabilite * risque.impact

        risques_serialises.append(
            {
                "id": risque.id,
                "scenario": risque.scenario,
                "score": score,
                "niveau": calculer_niveau(score),
                "proprietaire": risque.proprietaire,
            }
        )

    risques_par_activite = {}

    for risque in risques:
        for activite in risque.activites:
            if activite.id not in risques_par_activite:
                risques_par_activite[activite.id] = {
                    "activite_id": activite.id,
                    "activite": activite.nom,
                    "nombre_risques": 0,
                }

            risques_par_activite[activite.id][
                "nombre_risques"
            ] += 1

    niveaux = {
        "faible": 0,
        "modere": 0,
        "eleve": 0,
    }

    for risque in risques_serialises:
        niveaux[risque["niveau"]] += 1

    traitements_en_retard = sum(
        traitement_en_retard(traitement)
        for traitement in traitements
    )

    return {
        "indicateurs": {
            "total_risques": len(risques),
            "risques_faibles": niveaux["faible"],
            "risques_moderees": niveaux["modere"],
            "risques_eleves": niveaux["eleve"],
            "mesures_en_retard": traitements_en_retard,
        },
        "repartition_niveaux": niveaux,
        "risques_par_activite": sorted(
            risques_par_activite.values(),
            key=lambda item: item["nombre_risques"],
            reverse=True,
        ),
        "top_risques": risques_serialises[:3],
        "suivi_traitements": {
            "planifies": sum(
                traitement.statut == "planifie"
                for traitement in traitements
            ),
            "en_cours": sum(
                traitement.statut == "en_cours"
                for traitement in traitements
            ),
            "termines": sum(
                traitement.statut == "termine"
                for traitement in traitements
            ),
            "annules": sum(
                traitement.statut == "annule"
                for traitement in traitements
            ),
            "en_retard": traitements_en_retard,
        },
    }