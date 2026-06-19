import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, Numeric, Integer, DateTime, Enum, ForeignKey, Time, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class CampaignStatus(str, PyEnum):
    ACTIVE = "active"
    PAUSED = "paused"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    current_status = Column(Enum(CampaignStatus), nullable=False, default=CampaignStatus.ACTIVE)
    target_status = Column(Enum(CampaignStatus), nullable=True)
    is_managed = Column(Boolean, default=True)
    budget_limit = Column(Numeric(10, 2), nullable=True)
    spend_today = Column(Numeric(10, 2), default=0)
    stock_days_left = Column(Integer, nullable=True)
    stock_days_min = Column(Integer, nullable=True)
    schedule_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    schedules = relationship("CampaignSchedule", back_populates="campaign", cascade="all, delete-orphan")
    logs = relationship("RuleEvaluationLog", back_populates="campaign", cascade="all, delete-orphan")


class CampaignSchedule(Base):
    __tablename__ = "campaign_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    campaign = relationship("Campaign", back_populates="schedules")


class RuleEvaluationLog(Base):
    __tablename__ = "rule_evaluation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    triggered_rule = Column(String, nullable=True)
    previous_target = Column(Enum(CampaignStatus), nullable=True)
    new_target = Column(Enum(CampaignStatus), nullable=True)
    context = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    campaign = relationship("Campaign", back_populates="logs")
#ПЕРЕПРОВЕРИТЬ     