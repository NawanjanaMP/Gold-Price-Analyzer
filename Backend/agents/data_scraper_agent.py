"""
Agent 1: Data Scraper & Database Manager
Responsible for scraping gold price data from the website and storing in database
"""

import httpx
from bs4 import BeautifulSoup
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.database_models import GoldPrice
import re
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataScraperAgent:
    """Agent responsible for scraping and managing gold price data"""
    
    def __init__(self, db: Session):
        self.db = db
        self.url = "https://www.ideabeam.com/finance/rates/goldprice.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse_price(self, price_str: str) -> float:
        """Parse price string and convert to float"""
        # Remove 'Rs.' and commas, then convert to float
        cleaned = price_str.replace('Rs.', '').replace(',', '').strip()
        return float(cleaned)
    
    def parse_date(self, date_str: str) -> date:
        """Parse date string to date object"""
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            logger.error(f"Failed to parse date: {date_str}")
            return None
    
    async def scrape_gold_prices(self) -> List[Dict]:
        """Scrape gold prices from the website"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.url, headers=self.headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table containing historical data
            tables = soup.find_all('table')

            if not tables or len(tables) < 2:
                logger.error("Could not find the price table")
                return []

            # The second table contains historical data
            price_table = tables[1]
            rows = price_table.find_all('tr')[1:]  # Skip header row

            scraped_data = []

            for row_idx, row in enumerate(rows):
                cols = row.find_all(['th', 'td'])  # Include both th and td elements
                if len(cols) >= 5:
                    try:
                        date_text = cols[0].text.strip()

                        # Debug: log first few rows
                        if row_idx < 3:
                            logger.info(f"Row {row_idx}: Date='{date_text}', Col1='{cols[1].text.strip()}'")

                        parsed_date = self.parse_date(date_text)

                        if not parsed_date:
                            continue

                        price_data = {
                            'date': parsed_date,
                            'gold_ounce': self.parse_price(cols[1].text),
                            'carat_24_1gram': self.parse_price(cols[2].text),
                            'carat_22_1gram': self.parse_price(cols[3].text),
                            'carat_22_8grams': self.parse_price(cols[4].text),
                            'carat_21_1gram': self.parse_price(cols[5].text) if len(cols) > 5 else 0.0
                        }

                        scraped_data.append(price_data)
                    except Exception as e:
                        logger.error(f"Error parsing row {row_idx}: {e}")
                        continue

            logger.info(f"Successfully scraped {len(scraped_data)} price records")
            return scraped_data

        except Exception as e:
            logger.error(f"Error scraping website: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    def get_existing_dates(self) -> set:
        """Get all dates that already exist in the database"""
        existing_records = self.db.query(GoldPrice.date).all()
        return {record.date for record in existing_records}
    
    def store_prices(self, price_data: List[Dict]) -> Dict[str, int]:
        """Store scraped prices in database, avoiding duplicates"""
        existing_dates = self.get_existing_dates()
        
        new_records = 0
        updated_records = 0
        
        for data in price_data:
            if data['date'] in existing_dates:
                # Update existing record
                record = self.db.query(GoldPrice).filter(GoldPrice.date == data['date']).first()
                if record:
                    record.gold_ounce = data['gold_ounce']
                    record.carat_24_1gram = data['carat_24_1gram']
                    record.carat_22_1gram = data['carat_22_1gram']
                    record.carat_22_8grams = data['carat_22_8grams']
                    record.carat_21_1gram = data['carat_21_1gram']
                    record.updated_at = datetime.utcnow()
                    updated_records += 1
            else:
                # Insert new record
                new_record = GoldPrice(**data)
                self.db.add(new_record)
                new_records += 1
        
        self.db.commit()
        
        logger.info(f"Database update: {new_records} new records, {updated_records} updated records")
        
        return {
            'new_records': new_records,
            'updated_records': updated_records,
            'total_records': self.get_total_records()
        }
    
    def get_total_records(self) -> int:
        """Get total number of records in database"""
        return self.db.query(GoldPrice).count()
    
    def get_latest_record(self) -> Optional[GoldPrice]:
        """Get the most recent gold price record"""
        return self.db.query(GoldPrice).order_by(desc(GoldPrice.date)).first()
    
    async def sync_data(self) -> Dict[str, int]:
        """Main method to scrape and sync data"""
        logger.info("Starting data synchronization...")
        
        # Scrape data from website
        scraped_data = await self.scrape_gold_prices()
        
        if not scraped_data:
            logger.warning("No data scraped from website")
            return {'new_records': 0, 'updated_records': 0, 'total_records': self.get_total_records()}
        
        # Store in database
        result = self.store_prices(scraped_data)
        
        logger.info(f"Data synchronization complete: {result}")
        return result
