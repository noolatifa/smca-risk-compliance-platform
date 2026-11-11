from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.bia.models import BIA, BIAImpact
from backend.bia.schemas import BIACreate, BIAUpdate, StatutBIA
from backend.referentiel.models import Activite

HORIZONS_AUTORISES = {1, 4, 8, 24, 72}


def _obtenir_activite(
    db: Session,
    activite_id: int,
) -> Activite:
    activite = db.get(Activite, activite_id)

    if activite is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité introuvable.",
        )

    if activite.archive:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Impossible de créer une BIA pour une activité archivée.",
        )

    return activite


def _verifier_coherence(
    data: BIACreate,
) -> None:
    if data.statut == StatutBIA.VALIDE:
        champs_obligatoires = {
            "responsable": data.responsable,
            "heures_fonctionnement": data.heures_fonctionnement,
            "sites_concernes": data.sites_concernes,
            "mtpd_heures": data.mtpd_heures,
            "rto_heures": data.rto_heures,
            "capacite_minimale_pct": data.capacite_minimale_pct,
        }

        champs_manquants = [
            nom
            for nom, valeur in champs_obligatoires.items()
            if valeur is None
        ]

        if champs_manquants:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "Une BIA validée doit être complète. "
                    f"Champs manquants : {', '.join(champs_manquants)}."
                ),
            )

        if data.rto_heures >= data.mtpd_heures:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le RTO doit être strictement inférieur à la MTPD.",
            )

    horizons = [
        impact.horizon_heures
        for impact in data.impacts
    ]

    horizons_invalides = set(horizons) - HORIZONS_AUTORISES

    if horizons_invalides:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Les horizons autorisés sont : 1, 4, 8, 24 et 72 heures.",
        )

    if len(horizons) != len(set(horizons)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Un même horizon ne peut apparaître qu'une seule fois.",
        )


def _verifier_bia_complete(bia: BIA) -> None:
    champs_obligatoires = {
        "responsable": bia.responsable,
        "heures_fonctionnement": bia.heures_fonctionnement,
        "sites_concernes": bia.sites_concernes,
        "mtpd_heures": bia.mtpd_heures,
        "rto_heures": bia.rto_heures,
        "capacite_minimale_pct": bia.capacite_minimale_pct,
    }

    champs_manquants = [
        nom
        for nom, valeur in champs_obligatoires.items()
        if valeur is None
    ]

    if champs_manquants:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "La BIA est incomplète. "
                f"Champs manquants : {', '.join(champs_manquants)}."
            ),
        )

    if bia.rto_heures >= bia.mtpd_heures:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Le RTO doit être strictement inférieur à la MTPD.",
        )






def creer_bia(
    db: Session,
    data: BIACreate,
) -> BIA:
    _obtenir_activite(db, data.activite_id)
    _verifier_coherence(data)

    bia_existante = db.scalar(
        select(BIA).where(
            BIA.activite_id == data.activite_id,
        )
    )

    if bia_existante is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cette activité possède déjà une BIA.",
        )

    bia = BIA(
        activite_id=data.activite_id,
        responsable=data.responsable,
        heures_fonctionnement=data.heures_fonctionnement,
        sites_concernes=data.sites_concernes,
        periode_pointe=data.periode_pointe,
        mtpd_heures=data.mtpd_heures,
        justification_mtpd=data.justification_mtpd,
        rto_heures=data.rto_heures,
        capacite_minimale_pct=data.capacite_minimale_pct,
        rpo_heures=data.rpo_heures,
        justification_rpo=data.justification_rpo,
        statut=data.statut.value,
    )

    bia.impacts = [
        BIAImpact(
            horizon_heures=impact.horizon_heures,
            clients=impact.clients,
            operations=impact.operations,
            finances=impact.finances,
            engagements=impact.engagements,
            reputation=impact.reputation,
        )
        for impact in data.impacts
    ]

    db.add(bia)
    db.commit()
    db.refresh(bia)

    return bia

def modifier_bia(
    db: Session,
    bia_id: int,
    data: BIAUpdate,
) -> BIA:
    bia = obtenir_bia(db, bia_id)

    valeurs = data.model_dump(
        exclude_unset=True,
        exclude={"impacts"},
    )

    mtpd = valeurs.get("mtpd_heures", bia.mtpd_heures)
    rto = valeurs.get("rto_heures", bia.rto_heures)

    if mtpd is not None and rto is not None and rto >= mtpd:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Le RTO doit être strictement inférieur à la MTPD.",
        )

    for nom_champ, valeur in valeurs.items():
        setattr(bia, nom_champ, valeur)

    if data.impacts is not None:
        horizons = [
            impact.horizon_heures
            for impact in data.impacts
        ]

        if not set(horizons).issubset(HORIZONS_AUTORISES):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "Les horizons autorisés sont : "
                    "1, 4, 8, 24 et 72 heures."
                ),
            )

        if len(horizons) != len(set(horizons)):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Un même horizon ne peut apparaître qu'une seule fois.",
            )

        bia.impacts.clear()

        bia.impacts.extend(
            BIAImpact(
                horizon_heures=impact.horizon_heures,
                clients=impact.clients,
                operations=impact.operations,
                finances=impact.finances,
                engagements=impact.engagements,
                reputation=impact.reputation,
            )
            for impact in data.impacts
        )

    db.commit()
    db.refresh(bia)

    return bia

def obtenir_bia(
    db: Session,
    bia_id: int,
) -> BIA:
    bia = db.get(BIA, bia_id)

    if bia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BIA introuvable.",
        )

    return bia


def lister_bias(
    db: Session,
) -> list[BIA]:
    requete = select(BIA).order_by(BIA.id)

    return list(db.scalars(requete))





def soumettre_bia(
    db: Session,
    bia_id: int,
) -> BIA:
    bia = obtenir_bia(db, bia_id)

    if bia.statut not in {"brouillon", "a_corriger"}:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Seule une BIA en brouillon ou à corriger "
                "peut être soumise."
            ),
        )

    _verifier_bia_complete(bia)

    bia.statut = "soumis"

    db.commit()
    db.refresh(bia)

    return bia


def valider_bia(
    db: Session,
    bia_id: int,
) -> BIA:
    bia = obtenir_bia(db, bia_id)

    if bia.statut != "soumis":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seule une BIA soumise peut être validée.",
        )

    _verifier_bia_complete(bia)

    bia.statut = "valide"

    db.commit()
    db.refresh(bia)

    return bia


def demander_correction_bia(
    db: Session,
    bia_id: int,
) -> BIA:
    bia = obtenir_bia(db, bia_id)

    if bia.statut != "soumis":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seule une BIA soumise peut être renvoyée en correction.",
        )

    bia.statut = "a_corriger"

    db.commit()
    db.refresh(bia)

    return bia