from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.models import CampaignSchedule, RuleEvaluationLog
from app.database import get_db
from app.models import Campaign
from app.rules.rule_engine import RuleEngine

router = APIRouter()
rule_engine = RuleEngine()

"""Вычислить статус для одной кампании."""
@router.post("/campaigns/{campaign_id}/evaluate")
@router.post("/campaigns/{campaign_id}/evaluate")
def evaluate_campaign(campaign_id: UUID, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    schedules = db.query(CampaignSchedule).filter(CampaignSchedule.campaign_id == campaign_id).all()
    previous_target = campaign.target_status

    result = rule_engine.evaluate(campaign, schedules)

    campaign.target_status = result.target_status
    db.commit()

    log = RuleEvaluationLog(
        campaign_id=campaign.id,
        triggered_rule=result.rule_name,
        previous_target=previous_target,
        new_target=result.target_status,
        context={"details": result.details, "evaluated_at": datetime.now().isoformat()}
    )
    db.add(log)
    db.commit()

    return {
        "target_status": result.target_status,
        "triggered_rule": result.rule_name,
        "rule_details": result.details
    }

@router.post("/campaigns/evaluate-all")
def evaluate_all_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).filter(Campaign.is_managed == True).all()
    results = []

    for campaign in campaigns:
        schedules = db.query(CampaignSchedule).filter(CampaignSchedule.campaign_id == campaign.id).all()
        previous_target = campaign.target_status

        result = rule_engine.evaluate(campaign, schedules)

        campaign.target_status = result.target_status

        log = RuleEvaluationLog(
            campaign_id=campaign.id,
            triggered_rule=result.rule_name,
            previous_target=previous_target,
            new_target=result.target_status,
            context={"details": result.details, "evaluated_at": datetime.now().isoformat()}
        )
        db.add(log)

        results.append({
            "campaign_id": str(campaign.id),
            "target_status": result.target_status,
            "triggered_rule": result.rule_name
        })

    db.commit()

    return {"evaluated": len(results), "results": results}