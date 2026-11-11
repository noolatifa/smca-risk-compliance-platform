from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.exports import service

router = APIRouter(
    prefix="/exports",
    tags=["Exports"],
)


@router.get("/risques.csv")
def exporter_risques(
    db: Session = Depends(get_db),
):
    contenu = service.exporter_risques_csv(db)

    return StreamingResponse(
        iter([contenu]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": (
                "attachment; filename=risques.csv"
            )
        },
    )


@router.get("/traitements.csv")
def exporter_traitements(
    db: Session = Depends(get_db),
):
    contenu = service.exporter_traitements_csv(db)

    return StreamingResponse(
        iter([contenu]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": (
                "attachment; filename=traitements.csv"
            )
        },
    )
    
    
    
    
    
@router.get("/risques.pdf")
def exporter_risques_pdf(
    db: Session = Depends(get_db),
):
    contenu = service.exporter_risques_pdf(db)

    return StreamingResponse(
        iter([contenu]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                "attachment; filename=risques.pdf"
            )
        },
    )


@router.get("/traitements.pdf")
def exporter_traitements_pdf(
    db: Session = Depends(get_db),
):
    contenu = service.exporter_traitements_pdf(db)

    return StreamingResponse(
        iter([contenu]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                "attachment; filename=traitements.pdf"
            )
        },
    )
    
    
    
@router.get("/dashboard.pdf")
def exporter_dashboard_pdf(
    db: Session = Depends(get_db),
):
    contenu = service.exporter_dashboard_pdf(db)

    return StreamingResponse(
        iter([contenu]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                "attachment; filename=dashboard.pdf"
            )
        },
    )