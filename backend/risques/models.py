from __future__ import annotations

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.referentiel.models import Activite, Ressource


risque_activites = Table(
    "risque_activites",
    Base.metadata,
    Column(
        "risque_id",
        ForeignKey("risques.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activite_id",
        ForeignKey("activites.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


risque_ressources = Table(
    "risque_ressources",
    Base.metadata,
    Column(
        "risque_id",
        ForeignKey("risques.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "ressource_id",
        ForeignKey("ressources.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Risque(Base):
    __tablename__ = "risques"

    __table_args__ = (
        CheckConstraint(
            "probabilite BETWEEN 1 AND 4",
            name="ck_risque_probabilite",
        ),
        CheckConstraint(
            "impact BETWEEN 1 AND 4",
            name="ck_risque_impact",
        ),
        CheckConstraint(
            "score_criticite BETWEEN 1 AND 16",
            name="ck_risque_score",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    scenario: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    cause: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    menace: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    vulnerabilite: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    consequences: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    proprietaire: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    probabilite: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    impact: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    score_criticite: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    niveau: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    statut: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="brouillon",
    )

    activites: Mapped[list[Activite]] = relationship(
        secondary=risque_activites,
    )

    ressources: Mapped[list[Ressource]] = relationship(
        secondary=risque_ressources,
    )