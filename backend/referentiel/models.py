from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    false,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class Activite(Base):
    __tablename__ = "activites"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Règle métier : on archive, on ne supprime pas.
    archive: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false())

    dependances: Mapped[list[Dependance]] = relationship(back_populates="activite")


class Ressource(Base):
    __tablename__ = "ressources"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    type_ressource: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    archive: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false())

    dependances: Mapped[list[Dependance]] = relationship(back_populates="ressource")


class Dependance(Base):
    """Lien activité <-> ressource, qualifié (F02)."""

    __tablename__ = "dependances"
    __table_args__ = (
        UniqueConstraint("activite_id", "ressource_id", name="uq_dependance"),
        CheckConstraint("criticite BETWEEN 1 AND 4", name="ck_dependance_criticite"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    activite_id: Mapped[int] = mapped_column(
        ForeignKey("activites.id", ondelete="RESTRICT"), nullable=False
    )
    ressource_id: Mapped[int] = mapped_column(
        ForeignKey("ressources.id", ondelete="RESTRICT"), nullable=False
    )
    criticite: Mapped[int] = mapped_column(nullable=False)
    indispensable: Mapped[bool] = mapped_column(Boolean, default=True)
    alternative: Mapped[str | None] = mapped_column(Text, nullable=True)

    activite: Mapped[Activite] = relationship(back_populates="dependances")
    ressource: Mapped[Ressource] = relationship(back_populates="dependances")
