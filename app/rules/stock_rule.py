from typing import Dict, Any
from app.rules.base import BaseRule, RuleResult
from app.models import Campaign, CampaignStatus


class StockRule(BaseRule):
    @property
    def priority(self) -> int:
        return 2

    def evaluate(self, campaign: Campaign, context: Dict[str, Any] = None) -> RuleResult:
        if campaign.stock_days_min is None:
            return RuleResult(triggered=False)

        if campaign.stock_days_left is None or campaign.stock_days_left < campaign.stock_days_min:
            return RuleResult(
                triggered=True,
                target_status=CampaignStatus.PAUSED,
                rule_name="low_stock",
                details=(
                    f"Остатков: {campaign.stock_days_left or 0} дней "
                    f"(минимум: {campaign.stock_days_min} дней)"
                ),
            )

        return RuleResult(triggered=False)
#ПЕРЕПРОВЕРИТЬ