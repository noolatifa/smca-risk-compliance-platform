import csv
import io

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.risques.models import Risque
from backend.traitement.models import Traitement


def exporter_risques_csv(db: Session) -> str:
    risques = db.scalars(
        select(Risque)
        .where(Risque.statut == "valide")
        .order_by(Risque.score_criticite.desc())
    ).all()

    fichier = io.StringIO()
    fichier.write("\ufeff")

    writer = csv.writer(fichier, delimiter=";")

    writer.writerow(
        [
            "ID",
            "Scénario",
            "Cause",
            "Menace",
            "Vulnérabilité",
            "Conséquences",
            "Propriétaire",
            "Probabilité",
            "Impact",
            "Score",
            "Niveau",
            "Statut",
            "Activités",
            "Ressources",
        ]
    )

    for risque in risques:
        writer.writerow(
            [
                risque.id,
                risque.scenario,
                risque.cause,
                risque.menace,
                risque.vulnerabilite,
                risque.consequences,
                risque.proprietaire,
                risque.probabilite,
                risque.impact,
                risque.score_criticite,
                risque.niveau,
                risque.statut,
                ", ".join(
                    activite.nom
                    for activite in risque.activites
                ),
                ", ".join(
                    ressource.nom
                    for ressource in risque.ressources
                ),
            ]
        )

    return fichier.getvalue()


def exporter_traitements_csv(db: Session) -> str:
    traitements = db.scalars(
        select(Traitement)
        .order_by(Traitement.echeance)
    ).all()

    fichier = io.StringIO()
    fichier.write("\ufeff")

    writer = csv.writer(fichier, delimiter=";")

    writer.writerow(
        [
            "ID",
            "Risque ID",
            "Mesure",
            "Responsable",
            "Échéance",
            "Statut",
            "Description",
            "Commentaire",
            "Date de réalisation",
        ]
    )

    for traitement in traitements:
        writer.writerow(
            [
                traitement.id,
                traitement.risque_id,
                traitement.mesure,
                traitement.responsable,
                traitement.echeance,
                traitement.statut,
                traitement.description or "",
                traitement.commentaire or "",
                traitement.date_realisation or "",
            ]
        )

    return fichier.getvalue()