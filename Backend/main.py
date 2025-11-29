"""
FastAPI Main Application
Multi-Agent Gold Price Analyzer System
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime
from contextlib import asynccontextmanager
import logging

from database.connection import get_db, init_db
from agents.data_scraper_agent import DataScraperAgent
from agents.data_provider_agent import DataProviderAgent
from agents.price_tracker_agent import PriceTrackerAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    init_db()
    logger.info("Application startup complete")
    yield
    # Shutdown (if needed in future)
    logger.info("Application shutdown")


# Initialize FastAPI app
app = FastAPI(
    title="Gold Price Analyzer API",
    description="Multi-Agent System for Gold Price Analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Gold Price Analyzer API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== AGENT 1: DATA SCRAPER ENDPOINTS ====================

@app.post("/api/scrape/sync")
async def sync_gold_prices(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger data synchronization with the website
    This scrapes the website and updates the database
    """
    agent = DataScraperAgent(db)
    
    try:
        result = await agent.sync_data()
        return {
            "status": "success",
            "message": "Data synchronization completed",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error during sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scrape/status")
async def get_scraper_status(db: Session = Depends(get_db)):
    """Get current status of scraped data"""
    agent = DataScraperAgent(db)
    
    latest = agent.get_latest_record()
    total = agent.get_total_records()
    
    return {
        "total_records": total,
        "latest_record": latest.to_dict() if latest else None,
        "last_updated": latest.updated_at.isoformat() if latest and latest.updated_at else None
    }


# ==================== AGENT 2: DATA PROVIDER ENDPOINTS ====================

@app.get("/api/prices/latest")
async def get_latest_price(db: Session = Depends(get_db)):
    """Get the most recent gold price"""
    agent = DataProviderAgent(db)
    
    price = agent.get_latest_price()
    
    if not price:
        raise HTTPException(status_code=404, detail="No price data available")
    
    return {
        "status": "success",
        "data": price
    }


@app.get("/api/prices/period/{period}")
async def get_prices_by_period(
    period: str,
    db: Session = Depends(get_db)
):
    """
    Get prices for specific period
    period options: 'month', '3months', '6months', 'year', 'all'
    """
    valid_periods = ['month', '3months', '6months', 'year', 'all']
    
    if period not in valid_periods:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}"
        )
    
    agent = DataProviderAgent(db)
    prices = agent.get_prices_by_period(period)
    
    return {
        "status": "success",
        "period": period,
        "count": len(prices),
        "data": prices
    }


@app.get("/api/prices/monthly-aggregate")
async def get_monthly_aggregated_data(db: Session = Depends(get_db)):
    """Get monthly aggregated price data"""
    agent = DataProviderAgent(db)
    data = agent.get_monthly_aggregated_data()
    
    return {
        "status": "success",
        "count": len(data),
        "data": data
    }


@app.get("/api/prices/yearly-aggregate")
async def get_yearly_aggregated_data(db: Session = Depends(get_db)):
    """Get yearly aggregated price data"""
    agent = DataProviderAgent(db)
    data = agent.get_yearly_aggregated_data()
    
    return {
        "status": "success",
        "count": len(data),
        "data": data
    }


@app.get("/api/prices/statistics/{period}")
async def get_price_statistics(
    period: str = "3months",
    db: Session = Depends(get_db)
):
    """Get statistical summary for a given period"""
    agent = DataProviderAgent(db)
    stats = agent.get_price_statistics(period)
    
    return {
        "status": "success",
        "data": stats
    }


# ==================== AGENT 3: PRICE TRACKER ENDPOINTS ====================

@app.get("/api/tracking/weekly")
async def get_weekly_tracking(db: Session = Depends(get_db)):
    """Get weekly price change tracking"""
    agent = PriceTrackerAgent(db)
    tracking = agent.get_price_change_weekly()
    
    if not tracking:
        raise HTTPException(status_code=404, detail="Insufficient data for weekly tracking")
    
    return {
        "status": "success",
        "data": tracking
    }


@app.get("/api/tracking/monthly")
async def get_monthly_tracking(db: Session = Depends(get_db)):
    """Get monthly price change tracking"""
    agent = PriceTrackerAgent(db)
    tracking = agent.get_price_change_monthly()
    
    if not tracking:
        raise HTTPException(status_code=404, detail="Insufficient data for monthly tracking")
    
    return {
        "status": "success",
        "data": tracking
    }


@app.get("/api/tracking/all")
async def get_all_tracking(db: Session = Depends(get_db)):
    """Get comprehensive price tracking with alerts"""
    agent = PriceTrackerAgent(db)
    tracking = agent.get_all_price_tracking()
    
    return {
        "status": "success",
        "data": tracking
    }


@app.get("/api/alerts/recent")
async def get_recent_alerts(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent price alerts"""
    agent = PriceTrackerAgent(db)
    alerts = agent.get_recent_alerts(limit)
    
    return {
        "status": "success",
        "count": len(alerts),
        "data": alerts
    }


@app.post("/api/alerts/check")
async def check_alerts(db: Session = Depends(get_db)):
    """Manually trigger alert checking"""
    agent = PriceTrackerAgent(db)
    result = agent.check_and_generate_alerts()
    
    return {
        "status": "success",
        "data": result
    }


# ==================== COMBINED DASHBOARD ENDPOINT ====================

@app.get("/api/dashboard")
async def get_dashboard_data(db: Session = Depends(get_db)):
    """Get all dashboard data in one request"""
    
    # Initialize agents
    data_provider = DataProviderAgent(db)
    price_tracker = PriceTrackerAgent(db)
    scraper = DataScraperAgent(db)
    
    # Gather all data
    latest_price = data_provider.get_latest_price()
    statistics = data_provider.get_price_statistics('month')
    tracking = price_tracker.get_all_price_tracking()
    total_records = scraper.get_total_records()
    
    return {
        "status": "success",
        "data": {
            "latest_price": latest_price,
            "statistics": statistics,
            "tracking": tracking,
            "total_records": total_records,
            "last_updated": datetime.utcnow().isoformat()
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
