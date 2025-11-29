"""
Agent 2: Data Provider & Visualization Agent
Responsible for providing filtered data for frontend visualization
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from models.database_models import GoldPrice
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProviderAgent:
    """Agent responsible for providing data for visualization"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_daily_prices(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict]:
        """Get daily prices within date range"""
        query = self.db.query(GoldPrice).order_by(GoldPrice.date)
        
        if start_date:
            query = query.filter(GoldPrice.date >= start_date)
        if end_date:
            query = query.filter(GoldPrice.date <= end_date)
        
        records = query.all()
        return [record.to_dict() for record in records]
    
    def get_latest_price(self) -> Optional[Dict]:
        """Get the most recent gold price"""
        record = self.db.query(GoldPrice).order_by(desc(GoldPrice.date)).first()
        return record.to_dict() if record else None
    
    def get_prices_by_period(self, period: str) -> List[Dict]:
        """
        Get prices for specific period
        period options: 'month', '3months', '6months', 'year', 'all'
        """
        today = date.today()
        
        if period == 'month':
            start_date = today - timedelta(days=30)
        elif period == '3months':
            start_date = today - timedelta(days=90)
        elif period == '6months':
            start_date = today - timedelta(days=180)
        elif period == 'year':
            start_date = today - timedelta(days=365)
        elif period == 'all':
            start_date = None
        else:
            # Default to 1 month
            start_date = today - timedelta(days=30)
        
        return self.get_daily_prices(start_date=start_date, end_date=today)
    
    def get_monthly_aggregated_data(self) -> List[Dict]:
        """Get monthly aggregated data (average prices per month)"""
        records = self.db.query(GoldPrice).order_by(GoldPrice.date).all()
        
        # Group by year-month
        monthly_data = {}
        
        for record in records:
            year_month = f"{record.date.year}-{record.date.month:02d}"
            
            if year_month not in monthly_data:
                monthly_data[year_month] = {
                    'dates': [],
                    'gold_ounce': [],
                    'carat_24_1gram': [],
                    'carat_22_1gram': [],
                    'carat_22_8grams': [],
                    'carat_21_1gram': []
                }
            
            monthly_data[year_month]['dates'].append(record.date)
            monthly_data[year_month]['gold_ounce'].append(record.gold_ounce)
            monthly_data[year_month]['carat_24_1gram'].append(record.carat_24_1gram)
            monthly_data[year_month]['carat_22_1gram'].append(record.carat_22_1gram)
            monthly_data[year_month]['carat_22_8grams'].append(record.carat_22_8grams)
            monthly_data[year_month]['carat_21_1gram'].append(record.carat_21_1gram)
        
        # Calculate averages
        aggregated = []
        for month, data in sorted(monthly_data.items()):
            aggregated.append({
                'month': month,
                'avg_gold_ounce': sum(data['gold_ounce']) / len(data['gold_ounce']),
                'avg_carat_24_1gram': sum(data['carat_24_1gram']) / len(data['carat_24_1gram']),
                'avg_carat_22_1gram': sum(data['carat_22_1gram']) / len(data['carat_22_1gram']),
                'avg_carat_22_8grams': sum(data['carat_22_8grams']) / len(data['carat_22_8grams']),
                'avg_carat_21_1gram': sum(data['carat_21_1gram']) / len(data['carat_21_1gram']),
                'min_price': min(data['carat_22_1gram']),
                'max_price': max(data['carat_22_1gram']),
                'data_points': len(data['dates'])
            })
        
        return aggregated
    
    def get_yearly_aggregated_data(self) -> List[Dict]:
        """Get yearly aggregated data"""
        records = self.db.query(GoldPrice).order_by(GoldPrice.date).all()
        
        # Group by year
        yearly_data = {}
        
        for record in records:
            year = str(record.date.year)
            
            if year not in yearly_data:
                yearly_data[year] = {
                    'dates': [],
                    'gold_ounce': [],
                    'carat_24_1gram': [],
                    'carat_22_1gram': [],
                    'carat_22_8grams': [],
                    'carat_21_1gram': []
                }
            
            yearly_data[year]['dates'].append(record.date)
            yearly_data[year]['gold_ounce'].append(record.gold_ounce)
            yearly_data[year]['carat_24_1gram'].append(record.carat_24_1gram)
            yearly_data[year]['carat_22_1gram'].append(record.carat_22_1gram)
            yearly_data[year]['carat_22_8grams'].append(record.carat_22_8grams)
            yearly_data[year]['carat_21_1gram'].append(record.carat_21_1gram)
        
        # Calculate averages
        aggregated = []
        for year, data in sorted(yearly_data.items()):
            aggregated.append({
                'year': year,
                'avg_gold_ounce': sum(data['gold_ounce']) / len(data['gold_ounce']),
                'avg_carat_24_1gram': sum(data['carat_24_1gram']) / len(data['carat_24_1gram']),
                'avg_carat_22_1gram': sum(data['carat_22_1gram']) / len(data['carat_22_1gram']),
                'avg_carat_22_8grams': sum(data['carat_22_8grams']) / len(data['carat_22_8grams']),
                'avg_carat_21_1gram': sum(data['carat_21_1gram']) / len(data['carat_21_1gram']),
                'min_price': min(data['carat_22_1gram']),
                'max_price': max(data['carat_22_1gram']),
                'data_points': len(data['dates'])
            })
        
        return aggregated
    
    def get_price_statistics(self, period: str = '3months') -> Dict:
        """Get statistical summary of prices for a given period"""
        prices = self.get_prices_by_period(period)
        
        if not prices:
            return {}
        
        carat_22_prices = [p['carat_22_1gram'] for p in prices]
        
        return {
            'period': period,
            'count': len(prices),
            'current_price': prices[-1]['carat_22_1gram'] if prices else 0,
            'min_price': min(carat_22_prices),
            'max_price': max(carat_22_prices),
            'avg_price': sum(carat_22_prices) / len(carat_22_prices),
            'start_date': prices[0]['date'],
            'end_date': prices[-1]['date'],
            'price_change': prices[-1]['carat_22_1gram'] - prices[0]['carat_22_1gram'] if len(prices) > 1 else 0,
            'price_change_percentage': ((prices[-1]['carat_22_1gram'] - prices[0]['carat_22_1gram']) / prices[0]['carat_22_1gram'] * 100) if len(prices) > 1 and prices[0]['carat_22_1gram'] > 0 else 0
        }
