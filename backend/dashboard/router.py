from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.dashboard import service
from backend.dashboard.schemas import DashboardRead

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardRead,
)
def obtenir_dashboard(
    db: Session = Depends(get_db),
):
    return service.obtenir_dashboard(db)