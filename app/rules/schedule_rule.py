from typing import Dict, Any
from datetime import datetime
from app.rules.base import BaseRule, RuleResult
from app.models import Campaign, CampaignStatus


class ScheduleRule(BaseRule):
    @property
    def priority(self) -> int:
        return 1

    def evaluate(self, campaign: Campaign, context: Dict[str, Any] = None) -> RuleResult:
        if not campaign.schedule_enabled:
            return RuleResult(triggered=False)

        schedules = context.get("schedules", []) if context else []
        now = context.get("current_time", datetime.now()) if context else datetime.now()

        if not schedules:
            return RuleResult(triggered=False)

        current_day = now.weekday()
        current_time = now.time()

        for schedule in schedules:
            if (
                schedule.day_of_week == current_day
                and schedule.start_time <= current_time <= schedule.end_time
            ):
                return RuleResult(triggered=False)

        return RuleResult(
            triggered=True,
            target_status=CampaignStatus.PAUSED,
            rule_name="schedule",
            details=f"Текущее время {current_time.strftime('%H:%M')} вне активного окна",
        )
#ПЕРЕПРОВЕРИТЬ