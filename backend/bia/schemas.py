from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StatutBIA(str, Enum):
    BROUILLON = "brouillon"
    SOUMIS = "soumis"
    VALIDE = "valide"
    A_CORRIGER = "a_corriger"


class BIAImpactCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    horizon_heures: int = Field(
        ...,
        description="Horizon obligatoire : 1, 4, 8, 24 ou 72 heures.",
    )

    clients: str | None = None
    operations: str | None = None
    finances: str | None = None
    engagements: str | None = None
    reputation: str | None = None


class BIAImpactRead(BIAImpactCreate):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


class BIACreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    activite_id: int

    responsable: str | None = Field(
        default=None,
        max_length=150,
    )

    heures_fonctionnement: str | None = Field(
        default=None,
        max_length=100,
    )

    sites_concernes: str | None = None

    periode_pointe: str | None = Field(
        default=None,
        max_length=150,
    )

    mtpd_heures: float | None = Field(
        default=None,
        gt=0,
    )

    justification_mtpd: str | None = None

    rto_heures: float | None = Field(
        default=None,
        gt=0,
    )

    capacite_minimale_pct: int | None = Field(
        default=None,
        ge=1,
        le=100,
    )

    rpo_heures: float | None = Field(
        default=None,
        ge=0,
    )

    justification_rpo: str | None = None

    statut: StatutBIA = StatutBIA.BROUILLON

    impacts: list[BIAImpactCreate] = Field(
        default_factory=list,
    )


class BIARead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    activite_id: int
    responsable: str | None
    heures_fonctionnement: str | None
    sites_concernes: str | None
    periode_pointe: str | None
    mtpd_heures: float | None
    justification_mtpd: str | None
    rto_heures: float | None
    capacite_minimale_pct: int | None
    rpo_heures: float | None
    justification_rpo: str | None
    statut: StatutBIA
    impacts: list[BIAImpactRead] = Field(
        default_factory=list,
    )
    
    
    
    
class BIAUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    responsable: str | None = Field(
        default=None,
        max_length=150,
    )

    heures_fonctionnement: str | None = Field(
        default=None,
        max_length=100,
    )

    sites_concernes: str | None = None

    periode_pointe: str | None = Field(
        default=None,
        max_length=150,
    )

    mtpd_heures: float | None = Field(
        default=None,
        gt=0,
    )

    justification_mtpd: str | None = None

    rto_heures: float | None = Field(
        default=None,
        gt=0,
    )

    capacite_minimale_pct: int | None = Field(
        default=None,
        ge=1,
        le=100,
    )

    rpo_heures: float | None = Field(
        default=None,
        ge=0,
    )

    justification_rpo: str | None = None

    impacts: list[BIAImpactCreate] | None = None