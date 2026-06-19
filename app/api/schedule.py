from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.models import Campaign, CampaignSchedule
from app.schemas import ScheduleCreate, ScheduleResponse

router = APIRouter()


@router.put("/campaigns/{campaign_id}/schedule", response_model=List[ScheduleResponse])
def set_schedule(campaign_id: UUID, schedules: List[ScheduleCreate], db: Session = Depends(get_db)):
    """Установить расписание для кампании (заменяет все слоты)."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Удаляем старые слоты
    db.query(CampaignSchedule).filter(CampaignSchedule.campaign_id == campaign_id).delete()
    
    # Создаём новые
    new_schedules = []
    for schedule in schedules:
        db_schedule = CampaignSchedule(
            campaign_id=campaign_id,
            day_of_week=schedule.day_of_week,
            start_time=schedule.start_time,
            end_time=schedule.end_time
        )
        db.add(db_schedule)
        new_schedules.append(db_schedule)
    
    db.commit()
    return new_schedules


@router.get("/campaigns/{campaign_id}/schedule", response_model=List[ScheduleResponse])
def get_schedule(campaign_id: UUID, db: Session = Depends(get_db)):
    """Получить расписание кампании."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    schedules = db.query(CampaignSchedule).filter(CampaignSchedule.campaign_id == campaign_id).all()
    return schedules


@router.delete("/campaigns/{campaign_id}/schedule")
def delete_schedule(campaign_id: UUID, db: Session = Depends(get_db)):
    """Удалить расписание кампании."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db.query(CampaignSchedule).filter(CampaignSchedule.campaign_id == campaign_id).delete()
    db.commit()
    return {"message": "Schedule deleted"}