from sqlalchemy import Column, Integer, Float, String, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class GoldPrice(Base):
    """Model for storing daily gold prices"""
    __tablename__ = "gold_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    gold_ounce = Column(Float, nullable=False)
    carat_24_1gram = Column(Float, nullable=False)
    carat_22_1gram = Column(Float, nullable=False)
    carat_22_8grams = Column(Float, nullable=False)
    carat_21_1gram = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "gold_ounce": self.gold_ounce,
            "carat_24_1gram": self.carat_24_1gram,
            "carat_22_1gram": self.carat_22_1gram,
            "carat_22_8grams": self.carat_22_8grams,
            "carat_21_1gram": self.carat_21_1gram,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class PriceAlert(Base):
    """Model for storing price alerts and notifications"""
    __tablename__ = "price_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String, nullable=False)  # 'increase' or 'decrease'
    percentage = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    date_triggered = Column(Date, nullable=False)
    period_type = Column(String, nullable=False)  # 'week' or 'month'
    is_critical = Column(Integer, default=0)  # 1 if threshold exceeded (5% decrease or 10% increase)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "alert_type": self.alert_type,
            "percentage": self.percentage,
            "base_price": self.base_price,
            "current_price": self.current_price,
            "date_triggered": self.date_triggered.isoformat(),
            "period_type": self.period_type,
            "is_critical": bool(self.is_critical),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
