from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StatutRisque(str, Enum):
    BROUILLON = "brouillon"
    SOUMIS = "soumis"
    VALIDE = "valide"
    A_CORRIGER = "a_corriger"


class NiveauRisque(str, Enum):
    FAIBLE = "faible"
    MODERE = "modere"
    ELEVE = "eleve"


class RisqueCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    scenario: str = Field(min_length=1)
    cause: str = Field(min_length=1)
    menace: str = Field(min_length=1, max_length=150)
    vulnerabilite: str = Field(min_length=1)
    consequences: str = Field(min_length=1)
    proprietaire: str = Field(min_length=1, max_length=150)

    activite_ids: list[int] = Field(min_length=1)
    ressource_ids: list[int] = Field(default_factory=list)

    probabilite: int = Field(ge=1, le=4)
    impact: int = Field(ge=1, le=4)

    statut: StatutRisque = StatutRisque.BROUILLON


class RisqueUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    scenario: str | None = Field(default=None, min_length=1)
    cause: str | None = Field(default=None, min_length=1)
    menace: str | None = Field(default=None, max_length=150)
    vulnerabilite: str | None = Field(default=None, min_length=1)
    consequences: str | None = Field(default=None, min_length=1)
    proprietaire: str | None = Field(default=None, max_length=150)

    activite_ids: list[int] | None = None
    ressource_ids: list[int] | None = None

    probabilite: int | None = Field(
        default=None,
        ge=1,
        le=4,
    )

    impact: int | None = Field(
        default=None,
        ge=1,
        le=4,
    )


class RisqueRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    scenario: str
    cause: str
    menace: str
    vulnerabilite: str
    consequences: str
    proprietaire: str

    activite_ids: list[int]
    ressource_ids: list[int]

    probabilite: int
    impact: int
    score_criticite: int
    niveau: NiveauRisque
    statut: StatutRisque