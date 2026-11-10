from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from backend.risques.models import Risque


class Traitement(Base):
    __tablename__ = "traitements"

    __table_args__ = (
        CheckConstraint(
            "statut IN ('planifie', 'en_cours', 'termine', 'annule')",
            name="ck_traitement_statut",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    risque_id: Mapped[int] = mapped_column(
        ForeignKey("risques.id", ondelete="CASCADE"),
        nullable=False,
    )

    mesure: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    responsable: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    echeance: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    statut: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="planifie",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    commentaire: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    date_realisation: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    risque: Mapped[Risque] = relationship()