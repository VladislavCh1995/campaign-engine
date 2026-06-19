from abc import ABC,abstractmethod
from typing import Optional, Dict, Any
from app.models import Campaign, CampaignStatus

class RuleResult:
    """Результат проверки правила."""
    def __init__(
        self,
        triggered:bool,
        target_status: Optional[CampaignStatus] = None,
        rule_name: Optional[str] = None,
        details:Optional[str] = None,
    ):
        self.triggered = triggered
        self.target_status = target_status
        self.rule_name = rule_name
        self.details = details

class BaseRule(ABC): 
    """Базовый класс для всех правил."""

    @abstractmethod
    def evaluate(self, campaign: Campaign, context: Dict[str, Any] = None) -> RuleResult:
        pass
    
    @property
    @abstractmethod
    def priority(self) -> int:
        pass