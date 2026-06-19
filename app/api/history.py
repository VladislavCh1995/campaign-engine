from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.models import Campaign, RuleEvaluationLog
from app.schemas import EvaluationLogResponse

router = APIRouter()


@router.get("/campaigns/{campaign_id}/evaluation-history", response_model=List[EvaluationLogResponse])
def get_evaluation_history(
    campaign_id: UUID,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Получить историю вычислений для кампании.
    От новых к старым, с пагинацией (skip/limit).
    """
    # Проверяем, что кампания существует
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Запрашиваем логи с сортировкой по убыванию даты
    logs = (
        db.query(RuleEvaluationLog)
        .filter(RuleEvaluationLog.campaign_id == campaign_id)
        .order_by(RuleEvaluationLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return logs