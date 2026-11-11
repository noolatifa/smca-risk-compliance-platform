from sqlalchemy import (
    CheckConstraint,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.referentiel.models import Activite


class BIA(Base):
    __tablename__ = "bias"

    __table_args__ = (
        CheckConstraint(
            "mtpd_heures IS NULL OR mtpd_heures > 0",
            name="ck_bia_mtpd_positive",
        ),
        CheckConstraint(
            "rto_heures IS NULL OR rto_heures > 0",
            name="ck_bia_rto_positif",
        ),
        CheckConstraint(
            "rpo_heures IS NULL OR rpo_heures >= 0",
            name="ck_bia_rpo_positif",
        ),
        CheckConstraint(
            "capacite_minimale_pct IS NULL "
            "OR capacite_minimale_pct BETWEEN 1 AND 100",
            name="ck_bia_capacite_valide",
        ),
        CheckConstraint(
            "rto_heures IS NULL "
            "OR mtpd_heures IS NULL "
            "OR rto_heures < mtpd_heures",
            name="ck_bia_rto_inferieur_mtpd",
        ),
        CheckConstraint(
            "statut IN ('brouillon', 'soumis', 'valide', 'a_corriger')",
            name="ck_bia_statut",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    activite_id: Mapped[int] = mapped_column(
        ForeignKey("activites.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )

    responsable: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    heures_fonctionnement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    sites_concernes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    periode_pointe: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    mtpd_heures: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    justification_mtpd: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rto_heures: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    capacite_minimale_pct: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    rpo_heures: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    justification_rpo: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    statut: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="brouillon",
    )

    activite: Mapped[Activite] = relationship()

    impacts: Mapped[list["BIAImpact"]] = relationship(
        back_populates="bia",
        cascade="all, delete-orphan",
        order_by="BIAImpact.horizon_heures",
    )


class BIAImpact(Base):
    __tablename__ = "bia_impacts"

    __table_args__ = (
        UniqueConstraint(
            "bia_id",
            "horizon_heures",
            name="uq_impact_bia_horizon",
        ),
        CheckConstraint(
            "horizon_heures IN (1, 4, 8, 24, 72)",
            name="ck_impact_horizon",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    bia_id: Mapped[int] = mapped_column(
        ForeignKey("bias.id", ondelete="CASCADE"),
        nullable=False,
    )

    horizon_heures: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    clients: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    operations: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    finances: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    engagements: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reputation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    bia: Mapped[BIA] = relationship(
        back_populates="impacts",
    )