import csv
import io
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.dashboard.service import obtenir_dashboard
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



def _creer_pdf(
    titre: str,
    entetes: list[str],
    lignes: list[list],
) -> bytes:
    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )

    styles = getSampleStyleSheet()

    contenu = [
        Paragraph(titre, styles["Title"]),
        Spacer(1, 0.3 * cm),
        Paragraph(
            f"Financia - Généré le {date.today()}",
            styles["Normal"],
        ),
        Spacer(1, 0.5 * cm),
    ]

    tableau = [
        [Paragraph(str(entete), styles["BodyText"])
         for entete in entetes]
    ]

    for ligne in lignes:
        tableau.append(
            [
                Paragraph(str(cellule or ""), styles["BodyText"])
                for cellule in ligne
            ]
        )

    table = Table(tableau, repeatRows=1)

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4e78"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#eaf2f8"),
                    ],
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
            ]
        )
    )

    contenu.append(table)
    document.build(contenu)

    return buffer.getvalue()




def exporter_risques_pdf(db: Session) -> bytes:
    risques = db.scalars(
        select(Risque)
        .where(Risque.statut == "valide")
        .order_by(Risque.score_criticite.desc())
    ).all()

    lignes = [
        [
            risque.id,
            risque.scenario,
            risque.probabilite,
            risque.impact,
            risque.score_criticite,
            risque.niveau,
            risque.proprietaire,
        ]
        for risque in risques
    ]

    return _creer_pdf(
        "Cartographie des risques validés",
        [
            "ID",
            "Scénario",
            "Probabilité",
            "Impact",
            "Score",
            "Niveau",
            "Propriétaire",
        ],
        lignes,
    )


def exporter_traitements_pdf(db: Session) -> bytes:
    traitements = db.scalars(
        select(Traitement)
        .order_by(Traitement.echeance)
    ).all()

    lignes = [
        [
            traitement.id,
            traitement.risque_id,
            traitement.mesure,
            traitement.responsable,
            traitement.echeance,
            traitement.statut,
        ]
        for traitement in traitements
    ]

    return _creer_pdf(
        "Plan de traitement des risques",
        [
            "ID",
            "Risque",
            "Mesure",
            "Responsable",
            "Échéance",
            "Statut",
        ],
        lignes,
    )
    
    
    
    
#export du dashboard
def exporter_dashboard_pdf(db: Session) -> bytes:
    dashboard = obtenir_dashboard(db)

    indicateurs = dashboard["indicateurs"]
    suivi = dashboard["suivi_traitements"]

    lignes = [
        [
            "Total des risques",
            indicateurs["total_risques"],
        ],
        [
            "Risques faibles",
            indicateurs["risques_faibles"],
        ],
        [
            "Risques modérés",
            indicateurs["risques_moderees"],
        ],
        [
            "Risques élevés",
            indicateurs["risques_eleves"],
        ],
        [
            "Mesures en retard",
            indicateurs["mesures_en_retard"],
        ],
        [
            "Traitements planifiés",
            suivi["planifies"],
        ],
        [
            "Traitements en cours",
            suivi["en_cours"],
        ],
        [
            "Traitements terminés",
            suivi["termines"],
        ],
        [
            "Traitements annulés",
            suivi["annules"],
        ],
    ]

    return _creer_pdf(
        "Tableau de bord Financia",
        [
            "Indicateur",
            "Valeur",
        ],
        lignes,
    )