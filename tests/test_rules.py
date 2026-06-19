import pytest
import sys
import os

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.rules.management_rule import ManagementRule
from app.models import Campaign, CampaignStatus


def test_management_rule_off():
    rule = ManagementRule()
    campaign = Campaign(
        id="123e4567-e89b-12d3-a456-426614174000",
        name="Test",
        current_status=CampaignStatus.ACTIVE,
        is_managed=False
    )
    result = rule.evaluate(campaign)
    assert result.triggered is True
    assert result.target_status == CampaignStatus.ACTIVE
    assert result.rule_name == "management_off"


def test_management_rule_on():
    rule = ManagementRule()
    campaign = Campaign(
        id="123e4567-e89b-12d3-a456-426614174000",
        name="Test",
        current_status=CampaignStatus.ACTIVE,
        is_managed=True
    )
    result = rule.evaluate(campaign)
    assert result.triggered is False
    assert result.target_status is None