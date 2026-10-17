from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    email = Column(String)
    transaction_date = Column(Date)
    status = Column(String)
    country = Column(String)


class QualityRun(Base):
    __tablename__ = 'quality_runs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    rules_applied = Column(Integer, default=0)
    global_conformity_pct = Column(Float, default=0.0)
    ml_anomalies_detected = Column(Integer, default=0)
    status = Column(String, default='success')
    ml_not_covered_by_rules = Column(Integer, default=0)

    rule_results = relationship('RuleResult', back_populates='quality_run')


class RuleResult(Base):
    __tablename__ = 'rule_results'

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('quality_runs.id'), nullable=False)
    column = Column(String, nullable=False)
    rule = Column(String, nullable=False)
    conformity_pct = Column(Float, default=0.0)
    severity = Column(String)
    failed_count = Column(Integer, default=0)

    quality_run = relationship('QualityRun', back_populates='rule_results')
