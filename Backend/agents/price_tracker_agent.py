"""
Agent 3: Price Tracker & Alert Agent
Responsible for tracking price changes and generating alerts
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.database_models import GoldPrice, PriceAlert
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PriceTrackerAgent:
    """Agent responsible for tracking prices and generating alerts"""
    
    # Critical thresholds
    CRITICAL_DECREASE_THRESHOLD = 5.0  # 5% decrease is critical
    CRITICAL_INCREASE_THRESHOLD = 10.0  # 10% increase is critical
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_percentage_change(self, old_price: float, new_price: float) -> float:
        """Calculate percentage change between two prices"""
        if old_price == 0:
            return 0.0
        return ((new_price - old_price) / old_price) * 100
    
    def get_price_change_weekly(self, carat: str = '22') -> Optional[Dict]:
        """Analyze weekly price changes (7 days)"""
        today = date.today()
        week_ago = today - timedelta(days=7)

        # Get current price
        current_record = self.db.query(GoldPrice).order_by(desc(GoldPrice.date)).first()

        if not current_record:
            return None

        # Get price from week ago (or closest available)
        week_record = self.db.query(GoldPrice).filter(
            GoldPrice.date <= week_ago
        ).order_by(desc(GoldPrice.date)).first()

        if not week_record:
            return None

        # Select the appropriate price field based on carat
        if carat == '24':
            base_price = week_record.carat_24_1gram
            current_price = current_record.carat_24_1gram
        else:  # Default to 22 carat
            base_price = week_record.carat_22_1gram
            current_price = current_record.carat_22_1gram

        # Calculate change
        percentage_change = self.calculate_percentage_change(base_price, current_price)

        is_critical = False
        alert_type = 'increase' if percentage_change > 0 else 'decrease'

        if percentage_change <= -self.CRITICAL_DECREASE_THRESHOLD:
            is_critical = True
        elif percentage_change >= self.CRITICAL_INCREASE_THRESHOLD:
            is_critical = True

        return {
            'period_type': 'week',
            'base_date': week_record.date.isoformat(),
            'current_date': current_record.date.isoformat(),
            'base_price': base_price,
            'current_price': current_price,
            'price_change': current_price - base_price,
            'percentage_change': round(percentage_change, 2),
            'alert_type': alert_type,
            'is_critical': is_critical,
            'days_tracked': (current_record.date - week_record.date).days,
            'carat': carat
        }
    
    def get_price_change_monthly(self, carat: str = '22') -> Optional[Dict]:
        """Analyze monthly price changes (30 days)"""
        today = date.today()
        month_ago = today - timedelta(days=30)

        # Get current price
        current_record = self.db.query(GoldPrice).order_by(desc(GoldPrice.date)).first()

        if not current_record:
            return None

        # Get price from month ago (or closest available)
        month_record = self.db.query(GoldPrice).filter(
            GoldPrice.date <= month_ago
        ).order_by(desc(GoldPrice.date)).first()

        if not month_record:
            return None

        # Select the appropriate price field based on carat
        if carat == '24':
            base_price = month_record.carat_24_1gram
            current_price = current_record.carat_24_1gram
        else:  # Default to 22 carat
            base_price = month_record.carat_22_1gram
            current_price = current_record.carat_22_1gram

        # Calculate change
        percentage_change = self.calculate_percentage_change(base_price, current_price)

        is_critical = False
        alert_type = 'increase' if percentage_change > 0 else 'decrease'

        if percentage_change <= -self.CRITICAL_DECREASE_THRESHOLD:
            is_critical = True
        elif percentage_change >= self.CRITICAL_INCREASE_THRESHOLD:
            is_critical = True

        return {
            'period_type': 'month',
            'base_date': month_record.date.isoformat(),
            'current_date': current_record.date.isoformat(),
            'base_price': base_price,
            'current_price': current_price,
            'price_change': current_price - base_price,
            'percentage_change': round(percentage_change, 2),
            'alert_type': alert_type,
            'is_critical': is_critical,
            'days_tracked': (current_record.date - month_record.date).days,
            'carat': carat
        }
    
    def get_all_price_tracking(self) -> Dict:
        """Get comprehensive price tracking for both weekly and monthly periods for both carats"""
        # Get tracking data for both 22 and 24 carat
        weekly_22 = self.get_price_change_weekly('22')
        monthly_22 = self.get_price_change_monthly('22')
        weekly_24 = self.get_price_change_weekly('24')
        monthly_24 = self.get_price_change_monthly('24')

        # Generate alerts for 22 carat
        alerts_22 = []
        if weekly_22:
            if weekly_22['is_critical']:
                if weekly_22['alert_type'] == 'decrease':
                    alerts_22.append({
                        'severity': 'critical',
                        'message': f"⚠️ CRITICAL ALERT: 22 Carat gold price decreased by {abs(weekly_22['percentage_change'])}% in the past week!",
                        'data': weekly_22
                    })
                else:
                    alerts_22.append({
                        'severity': 'critical',
                        'message': f"🚀 CRITICAL ALERT: 22 Carat gold price increased by {weekly_22['percentage_change']}% in the past week!",
                        'data': weekly_22
                    })
            else:
                alerts_22.append({
                    'severity': 'info',
                    'message': f"Weekly change: {'+' if weekly_22['percentage_change'] > 0 else ''}{weekly_22['percentage_change']}%",
                    'data': weekly_22
                })

        if monthly_22:
            if monthly_22['is_critical']:
                if monthly_22['alert_type'] == 'decrease':
                    alerts_22.append({
                        'severity': 'critical',
                        'message': f"⚠️ CRITICAL ALERT: 22 Carat gold price decreased by {abs(monthly_22['percentage_change'])}% in the past month!",
                        'data': monthly_22
                    })
                else:
                    alerts_22.append({
                        'severity': 'critical',
                        'message': f"🚀 CRITICAL ALERT: 22 Carat gold price increased by {monthly_22['percentage_change']}% in the past month!",
                        'data': monthly_22
                    })
            else:
                alerts_22.append({
                    'severity': 'info',
                    'message': f"Monthly change: {'+' if monthly_22['percentage_change'] > 0 else ''}{monthly_22['percentage_change']}%",
                    'data': monthly_22
                })

        # Generate alerts for 24 carat
        alerts_24 = []
        if weekly_24:
            if weekly_24['is_critical']:
                if weekly_24['alert_type'] == 'decrease':
                    alerts_24.append({
                        'severity': 'critical',
                        'message': f"⚠️ CRITICAL ALERT: 24 Carat gold price decreased by {abs(weekly_24['percentage_change'])}% in the past week!",
                        'data': weekly_24
                    })
                else:
                    alerts_24.append({
                        'severity': 'critical',
                        'message': f"🚀 CRITICAL ALERT: 24 Carat gold price increased by {weekly_24['percentage_change']}% in the past week!",
                        'data': weekly_24
                    })
            else:
                alerts_24.append({
                    'severity': 'info',
                    'message': f"Weekly change: {'+' if weekly_24['percentage_change'] > 0 else ''}{weekly_24['percentage_change']}%",
                    'data': weekly_24
                })

        if monthly_24:
            if monthly_24['is_critical']:
                if monthly_24['alert_type'] == 'decrease':
                    alerts_24.append({
                        'severity': 'critical',
                        'message': f"⚠️ CRITICAL ALERT: 24 Carat gold price decreased by {abs(monthly_24['percentage_change'])}% in the past month!",
                        'data': monthly_24
                    })
                else:
                    alerts_24.append({
                        'severity': 'critical',
                        'message': f"🚀 CRITICAL ALERT: 24 Carat gold price increased by {monthly_24['percentage_change']}% in the past month!",
                        'data': monthly_24
                    })
            else:
                alerts_24.append({
                    'severity': 'info',
                    'message': f"Monthly change: {'+' if monthly_24['percentage_change'] > 0 else ''}{monthly_24['percentage_change']}%",
                    'data': monthly_24
                })

        return {
            'carat_22': {
                'weekly_tracking': weekly_22,
                'monthly_tracking': monthly_22,
                'alerts': alerts_22,
                'has_critical_alerts': any(alert['severity'] == 'critical' for alert in alerts_22)
            },
            'carat_24': {
                'weekly_tracking': weekly_24,
                'monthly_tracking': monthly_24,
                'alerts': alerts_24,
                'has_critical_alerts': any(alert['severity'] == 'critical' for alert in alerts_24)
            },
            # For backward compatibility, keep the default 22 carat data at root level
            'weekly_tracking': weekly_22,
            'monthly_tracking': monthly_22,
            'alerts': alerts_22,
            'has_critical_alerts': any(alert['severity'] == 'critical' for alert in alerts_22) if alerts_22 else False
        }
    
    def save_alert(self, alert_data: Dict) -> PriceAlert:
        """Save alert to database"""
        alert = PriceAlert(
            alert_type=alert_data['alert_type'],
            percentage=alert_data['percentage_change'],
            base_price=alert_data['base_price'],
            current_price=alert_data['current_price'],
            date_triggered=datetime.strptime(alert_data['current_date'], '%Y-%m-%d').date(),
            period_type=alert_data['period_type'],
            is_critical=1 if alert_data['is_critical'] else 0
        )
        
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        
        return alert
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts from database"""
        alerts = self.db.query(PriceAlert).order_by(
            desc(PriceAlert.created_at)
        ).limit(limit).all()
        
        return [alert.to_dict() for alert in alerts]
    
    def check_and_generate_alerts(self) -> Dict:
        """Main method to check prices and generate alerts if thresholds are met"""
        tracking_data = self.get_all_price_tracking()
        
        # Save critical alerts to database
        if tracking_data['weekly_tracking'] and tracking_data['weekly_tracking']['is_critical']:
            self.save_alert(tracking_data['weekly_tracking'])
        
        if tracking_data['monthly_tracking'] and tracking_data['monthly_tracking']['is_critical']:
            self.save_alert(tracking_data['monthly_tracking'])
        
        logger.info(f"Alert check complete. Critical alerts: {tracking_data['has_critical_alerts']}")
        
        return tracking_data
