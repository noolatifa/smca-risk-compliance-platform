from pydantic import BaseModel


class IndicateursDashboard(BaseModel):
    total_risques: int
    risques_faibles: int
    risques_moderees: int
    risques_eleves: int
    mesures_en_retard: int


class RepartitionNiveau(BaseModel):
    faible: int
    modere: int
    eleve: int


class RisquesParActivite(BaseModel):
    activite_id: int
    activite: str
    nombre_risques: int


class RisquePrioritaire(BaseModel):
    id: int
    scenario: str
    score: int
    niveau: str
    proprietaire: str


class SuiviTraitements(BaseModel):
    planifies: int
    en_cours: int
    termines: int
    annules: int
    en_retard: int


class DashboardRead(BaseModel):
    indicateurs: IndicateursDashboard
    repartition_niveaux: RepartitionNiveau
    risques_par_activite: list[RisquesParActivite]
    top_risques: list[RisquePrioritaire]
    suivi_traitements: SuiviTraitements