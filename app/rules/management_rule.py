from typing import Dict, Any
from app.rules.base import BaseRule, RuleResult
from app.models import Campaign, CampaignStatus


class ManagementRule(BaseRule):
    @property
    def priority(self) -> int:
        return 0

    def evaluate(self, campaign: Campaign, context: Dict[str, Any] = None) -> RuleResult:
        if not campaign.is_managed:
            return RuleResult(
                triggered=True,
                target_status=campaign.current_status,
                rule_name="management_off",
                details="Автоматическое управление выключено",
            )
        return RuleResult(triggered=False)

#ПЕРЕПРОВЕРИТЬ