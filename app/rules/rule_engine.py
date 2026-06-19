from typing import List, Dict, Any
from datetime import datetime
from app.rules.base import BaseRule, RuleResult
from app.rules.management_rule import ManagementRule
from app.rules.schedule_rule import ScheduleRule
from app.rules.stock_rule import StockRule
from app.rules.budget_rule import BudgetRule
from app.models import Campaign, CampaignStatus
from app.models import CampaignSchedule


class RuleEngine:
    def __init__(self):
        self.rules: List[BaseRule] = [
            ManagementRule(),
            ScheduleRule(),
            StockRule(),
            BudgetRule(),
        ]

    def evaluate(
        self,
        campaign: Campaign,
        schedules: List[CampaignSchedule] = None,
        current_time: datetime = None,
    ) -> RuleResult:
        if not campaign.is_managed:
            return RuleResult(
                triggered=False,
                target_status=campaign.current_status,
                rule_name=None,
                details="Управление выключено",
            )

        context = {
            "schedules": schedules or [],
            "current_time": current_time or datetime.now(),
        }

        for rule in self.rules:
            result = rule.evaluate(campaign, context)
            if result.triggered:
                return result

        return RuleResult(
            triggered=False,
            target_status=CampaignStatus.ACTIVE,
            rule_name=None,
            details="Нет ограничений",
        )
#ПЕРЕПРОВЕРИТЬ    