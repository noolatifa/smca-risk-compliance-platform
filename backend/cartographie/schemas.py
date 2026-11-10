from pydantic import BaseModel, ConfigDict


class CaseHeatmap(BaseModel):
    probabilite: int
    impact: int
    score: int
    niveau: str
    nombre_risques: int
    risques_ids: list[int]


class RisqueCartographieRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario: str
    probabilite: int
    impact: int
    score_criticite: int
    niveau: str
    proprietaire: str
    statut: str


class CartographieRead(BaseModel):
    matrice: list[CaseHeatmap]
    risques: list[RisqueCartographieRead]
    total_risques: int
    risques_faibles: int
    risques_moderees: int
    risques_eleves: int


class StatistiquesCartographieRead(BaseModel):
    total_risques: int
    risques_faibles: int
    risques_moderees: int
    risques_eleves: int
    top_risques: list[RisqueCartographieRead]