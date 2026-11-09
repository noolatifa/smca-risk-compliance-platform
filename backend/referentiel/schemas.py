from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TypeRessource(str, Enum):
    personne = "personne"
    local = "local"
    liquidites = "liquidites"
    electricite = "electricite"
    telecommunications = "telecommunications"
    application = "application"
    base_de_donnees = "base_de_donnees"
    authentification = "authentification"
    fournisseur = "fournisseur"


class _Entree(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        use_enum_values=True,
    )


class _Lecture(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ActiviteCreate(_Entree):
    nom: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)


class ActiviteRead(_Lecture):
    id: int
    nom: str
    description: str | None
    archive: bool


class RessourceCreate(_Entree):
    nom: str = Field(min_length=1, max_length=150)
    type_ressource: TypeRessource
    description: str | None = Field(default=None, max_length=1000)


class RessourceRead(_Lecture):
    id: int
    nom: str
    type_ressource: str
    description: str | None
    archive: bool


class DependanceCreate(_Entree):
    activite_id: int
    ressource_id: int
    criticite: int = Field(ge=1, le=4)
    indispensable: bool = True
    alternative: str | None = Field(default=None, max_length=1000)


class DependanceRead(_Lecture):
    id: int
    activite_id: int
    ressource_id: int
    criticite: int
    indispensable: bool
    alternative: str | None
