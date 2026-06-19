from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict
from uuid import UUID
from app.models import CampaignStatus
from datetime import time


class CampaignBase(BaseModel):
    name: str
    current_status: CampaignStatus = CampaignStatus.ACTIVE
    is_managed: bool = True
    budget_limit: Optional[Any] = None
    spend_today: Any = 0
    stock_days_left: Optional[int] = None
    stock_days_min: Optional[int] = None
    schedule_enabled: bool = False


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    current_status: Optional[CampaignStatus] = None
    is_managed: Optional[bool] = None
    budget_limit: Optional[Any] = None
    spend_today: Optional[Any] = None
    stock_days_left: Optional[int] = None
    stock_days_min: Optional[int] = None
    schedule_enabled: Optional[bool] = None


class CampaignResponse(CampaignBase):
    id: UUID
    target_status: Optional[CampaignStatus] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ScheduleCreate(BaseModel):
    day_of_week: int  # 0=пн, 6=вс
    start_time: time
    end_time: time


class ScheduleResponse(ScheduleCreate):
    id: UUID
    campaign_id: UUID

    class Config:
        from_attributes = True

class EvaluationLogResponse(BaseModel):
    id: UUID
    campaign_id: UUID
    triggered_rule: Optional[str] = None
    previous_target: Optional[CampaignStatus] = None
    new_target: Optional[CampaignStatus] = None
    context: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True        
#ПЕРЕПРОВЕРИТЬ 