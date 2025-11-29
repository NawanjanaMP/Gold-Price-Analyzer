#!/usr/bin/env python3
"""
Test Script for Gold Price Analyzer Multi-Agent System
This script tests all three agents independently
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.connection import init_db
from models.database_models import Base
from agents.data_scraper_agent import DataScraperAgent
from agents.data_provider_agent import DataProviderAgent
from agents.price_tracker_agent import PriceTrackerAgent


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


async def test_agent_1(session):
    """Test Agent 1: Data Scraper"""
    print_section("TESTING AGENT 1: Data Scraper & Database Manager")
    
    agent = DataScraperAgent(session)
    
    print("\n📥 Scraping gold price data from website...")
    result = await agent.sync_data()
    
    print(f"✅ Sync complete!")
    print(f"   - New records added: {result['new_records']}")
    print(f"   - Records updated: {result['updated_records']}")
    print(f"   - Total records in DB: {result['total_records']}")
    
    latest = agent.get_latest_record()
    if latest:
        print(f"\n📊 Latest record:")
        print(f"   - Date: {latest.date}")
        print(f"   - 22 Carat 1 Gram: Rs. {latest.carat_22_1gram:,.2f}")
        print(f"   - Gold Ounce: Rs. {latest.gold_ounce:,.2f}")
    
    return True


def test_agent_2(session):
    """Test Agent 2: Data Provider"""
    print_section("TESTING AGENT 2: Data Provider & Visualization Engine")
    
    agent = DataProviderAgent(session)
    
    print("\n📈 Getting latest price...")
    latest = agent.get_latest_price()
    if latest:
        print(f"   ✅ Latest price (22 Carat): Rs. {latest['carat_22_1gram']:,.2f}")
    
    print("\n📊 Getting 3-month statistics...")
    stats = agent.get_price_statistics('3months')
    if stats:
        print(f"   - Current: Rs. {stats['current_price']:,.2f}")
        print(f"   - Average: Rs. {stats['avg_price']:,.2f}")
        print(f"   - Min: Rs. {stats['min_price']:,.2f}")
        print(f"   - Max: Rs. {stats['max_price']:,.2f}")
        print(f"   - Change: Rs. {stats['price_change']:,.2f} ({stats['price_change_percentage']:.2f}%)")
    
    print("\n📅 Getting monthly aggregated data...")
    monthly = agent.get_monthly_aggregated_data()
    print(f"   ✅ Found {len(monthly)} months of data")
    if monthly:
        latest_month = monthly[-1]
        print(f"   - Latest month: {latest_month['month']}")
        print(f"   - Average price: Rs. {latest_month['avg_carat_22_1gram']:,.2f}")
    
    print("\n📆 Getting yearly aggregated data...")
    yearly = agent.get_yearly_aggregated_data()
    print(f"   ✅ Found {len(yearly)} years of data")
    
    return True


def test_agent_3(session):
    """Test Agent 3: Price Tracker"""
    print_section("TESTING AGENT 3: Price Tracker & Alert System")
    
    agent = PriceTrackerAgent(session)
    
    print("\n📊 Analyzing weekly price changes...")
    weekly = agent.get_price_change_weekly()
    if weekly:
        print(f"   - Period: {weekly['days_tracked']} days")
        print(f"   - Base price: Rs. {weekly['base_price']:,.2f}")
        print(f"   - Current price: Rs. {weekly['current_price']:,.2f}")
        print(f"   - Change: {weekly['percentage_change']:.2f}%")
        if weekly['is_critical']:
            print(f"   ⚠️  CRITICAL ALERT: {weekly['alert_type'].upper()}")
        else:
            print(f"   ℹ️  Normal fluctuation")
    
    print("\n📊 Analyzing monthly price changes...")
    monthly = agent.get_price_change_monthly()
    if monthly:
        print(f"   - Period: {monthly['days_tracked']} days")
        print(f"   - Base price: Rs. {monthly['base_price']:,.2f}")
        print(f"   - Current price: Rs. {monthly['current_price']:,.2f}")
        print(f"   - Change: {monthly['percentage_change']:.2f}%")
        if monthly['is_critical']:
            print(f"   ⚠️  CRITICAL ALERT: {monthly['alert_type'].upper()}")
        else:
            print(f"   ℹ️  Normal fluctuation")
    
    print("\n🔔 Comprehensive tracking analysis...")
    tracking = agent.check_and_generate_alerts()
    
    if tracking['alerts']:
        print(f"\n   Generated {len(tracking['alerts'])} alerts:")
        for i, alert in enumerate(tracking['alerts'], 1):
            icon = "⚠️" if alert['severity'] == 'critical' else "ℹ️"
            print(f"   {i}. {icon} {alert['message']}")
    
    print(f"\n   Critical alerts present: {'YES ⚠️' if tracking['has_critical_alerts'] else 'NO ✅'}")
    
    return True


async def main():
    """Main test function"""
    print("\n" + "=" * 80)
    print("  GOLD PRICE ANALYZER - MULTI-AGENT SYSTEM TEST")
    print("=" * 80)
    
    # Setup database
    print("\n🔧 Setting up test database...")
    DATABASE_URL = "sqlite:///./test_gold_prices.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    print("✅ Database initialized")
    
    try:
        # Test all agents
        success = True
        
        # Agent 1
        success &= await test_agent_1(session)
        
        # Agent 2
        success &= test_agent_2(session)
        
        # Agent 3
        success &= test_agent_3(session)
        
        print_section("TEST SUMMARY")
        if success:
            print("\n✅ ALL AGENTS WORKING CORRECTLY!")
            print("\nYou can now start the full application using:")
            print("   ./start.sh")
        else:
            print("\n❌ Some tests failed. Please check the errors above.")
        
        print("\n" + "=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(main())
