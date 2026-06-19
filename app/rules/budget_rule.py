from typing import Dict, Any
from app.rules.base import BaseRule, RuleResult
from app.models import Campaign, CampaignStatus


class BudgetRule(BaseRule):
    @property
    def priority(self) -> int:
        return 3

    def evaluate(self, campaign: Campaign, context: Dict[str, Any] = None) -> RuleResult:
        if campaign.budget_limit is None:
            return RuleResult(triggered=False)

        if campaign.spend_today >= campaign.budget_limit:
            return RuleResult(
                triggered=True,
                target_status=CampaignStatus.PAUSED,
                rule_name="budget_exceeded",
                details=f"Расход: {campaign.spend_today} руб. (лимит: {campaign.budget_limit} руб.)",
            )

        return RuleResult(triggered=False)
#ПЕРЕПРОВЕРИТЬ    