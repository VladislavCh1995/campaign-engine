from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from decimal import Decimal

from app.database import get_db
from app.models import Campaign
from app.schemas import CampaignCreate, CampaignUpdate, CampaignResponse

router = APIRouter()


def to_decimal(value):
    """Преобразует значение в Decimal, если оно не None."""
    if value is None:
        return None
    return Decimal(str(value))


@router.post("/campaigns", response_model=CampaignResponse, status_code=201)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    data = campaign.model_dump()
    
    # Преобразуем в Decimal
    if 'budget_limit' in data:
        data['budget_limit'] = to_decimal(data['budget_limit'])
    if 'spend_today' in data:
        data['spend_today'] = to_decimal(data['spend_today']) or Decimal('0')
    
    db_campaign = Campaign(**data)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


@router.get("/campaigns", response_model=List[CampaignResponse])
def list_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).offset(skip).limit(limit).all()
    return campaigns


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: UUID, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.patch("/campaigns/{campaign_id}", response_model=CampaignResponse)
def update_campaign(campaign_id: UUID, update: CampaignUpdate, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    data = update.model_dump(exclude_unset=True)
    
    # Преобразуем в Decimal
    if 'budget_limit' in data:
        data['budget_limit'] = to_decimal(data['budget_limit'])
    if 'spend_today' in data:
        data['spend_today'] = to_decimal(data['spend_today']) or Decimal('0')
    
    for field, value in data.items():
        setattr(campaign, field, value)
    
    db.commit()
    db.refresh(campaign)
    return campaign