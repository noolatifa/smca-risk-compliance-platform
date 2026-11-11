from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StatutTraitement(str, Enum):
    PLANIFIE = "planifie"
    EN_COURS = "en_cours"
    TERMINE = "termine"
    ANNULE = "annule"


class TraitementCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    risque_id: int

    mesure: str = Field(
        min_length=1,
    )

    responsable: str = Field(
        min_length=1,
        max_length=150,
    )

    echeance: date

    statut: StatutTraitement = StatutTraitement.PLANIFIE

    description: str | None = None

    commentaire: str | None = None

    date_realisation: date | None = None

@model_validator(mode="after")
def verifier_realisation(self):
    if (
        self.statut == StatutTraitement.TERMINE
        and self.date_realisation is None
    ):
        raise ValueError(
            "La date de réalisation est obligatoire "
            "pour un traitement terminé."
        )

    return self


class TraitementUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    mesure: str | None = Field(
        default=None,
        min_length=1,
    )

    responsable: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    echeance: date | None = None

    statut: StatutTraitement | None = None

    description: str | None = None

    commentaire: str | None = None

    date_realisation: date | None = None


class TraitementRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    risque_id: int
    mesure: str
    responsable: str
    echeance: date
    statut: StatutTraitement
    description: str | None
    commentaire: str | None
    date_realisation: date | None
    en_retard: bool


class TraitementDashboardRead(BaseModel):
    total: int
    planifies: int
    en_cours: int
    termines: int
    annules: int
    en_retard: int