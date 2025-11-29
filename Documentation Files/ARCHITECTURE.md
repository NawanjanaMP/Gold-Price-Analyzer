# 🏗️ System Architecture - Gold Price Analyzer

## Overview

This is a **Multi-Agent System** built with modern web technologies to provide comprehensive gold price analysis with real-time data scraping, intelligent tracking, and beautiful visualization.

## 📐 Architecture Diagram (Text Format)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (React + Tailwind CSS)                       │
│                                                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │   Dashboard  │ │    Charts    │ │    Alerts    │           │
│  │   Component  │ │  (Recharts)  │ │   Display    │           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         │
┌────────────────────────┴────────────────────────────────────────┐
│                     FASTAPI BACKEND                             │
│                   (Python 3.8+)                                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API ENDPOINTS                          │  │
│  │  /api/scrape/*  /api/prices/*  /api/tracking/*          │  │
│  └──────────┬──────────┬──────────────┬─────────────────────┘  │
│             │          │              │                          │
│  ┌──────────▼─┐ ┌─────▼──────┐ ┌────▼──────────┐              │
│  │  AGENT 1   │ │  AGENT 2   │ │   AGENT 3     │              │
│  │            │ │            │ │               │              │
│  │   Data     │ │   Data     │ │    Price      │              │
│  │  Scraper   │ │  Provider  │ │   Tracker     │              │
│  │            │ │            │ │               │              │
│  └──────┬─────┘ └─────┬──────┘ └────┬──────────┘              │
│         │             │             │                          │
└─────────┼─────────────┼─────────────┼──────────────────────────┘
          │             │             │
          └─────────────┴─────────────┘
                        │
          ┌─────────────▼─────────────┐
          │   SQLite DATABASE         │
          │                           │
          │  ┌──────────────────────┐ │
          │  │  gold_prices table   │ │
          │  │  - Historical data   │ │
          │  └──────────────────────┘ │
          │  ┌──────────────────────┐ │
          │  │  price_alerts table  │ │
          │  │  - Alert history     │ │
          │  └──────────────────────┘ │
          └───────────────────────────┘
                        ▲
                        │
          ┌─────────────┴─────────────┐
          │    EXTERNAL DATA SOURCE   │
          │  ideabeam.com/gold-price  │
          └───────────────────────────┘
```

## 🧩 Component Breakdown

### 1. Frontend Layer (React)

**Technology Stack:**
- React 18.2.0
- Vite (Build tool)
- Tailwind CSS (Styling)
- Recharts (Data visualization)
- Lucide React (Icons)

**Components:**
```
GoldPriceAnalyzer (Main Component)
├── Header Section
│   ├── Title
│   └── Sync Button
├── Current Price Display
│   ├── 22 Carat 1 Gram Card
│   ├── 22 Carat 8 Grams Card
│   ├── 24 Carat 1 Gram Card
│   └── Gold Ounce Card
├── Alerts Section
│   └── Alert Cards (Dynamic)
├── Chart Section
│   ├── Period Selector Buttons
│   ├── View Mode Buttons
│   └── Responsive Chart (Recharts)
└── Statistics Section
    ├── Current Price
    ├── Average Price
    ├── Min/Max Prices
    └── Price Change
```

**State Management:**
```javascript
useState hooks:
- priceData: Array of price records
- latestPrice: Most recent price object
- tracking: Tracking and alert data
- statistics: Statistical summaries
- selectedPeriod: Active time period
- viewMode: daily/monthly/yearly
- loading: Loading state
- syncing: Sync operation state
```

### 2. Backend Layer (FastAPI)

**Technology Stack:**
- FastAPI 0.104.1
- Uvicorn (ASGI server)
- SQLAlchemy 2.0.23 (ORM)
- AsyncIO (Async operations)
- BeautifulSoup4 (Web scraping)
- httpx (HTTP client)

**API Structure:**
```
FastAPI Application (main.py)
├── CORS Middleware
├── Startup Event (Database init)
├── Root Endpoint (Health check)
├── Agent 1 Endpoints
│   ├── POST /api/scrape/sync
│   └── GET /api/scrape/status
├── Agent 2 Endpoints
│   ├── GET /api/prices/latest
│   ├── GET /api/prices/period/{period}
│   ├── GET /api/prices/monthly-aggregate
│   ├── GET /api/prices/yearly-aggregate
│   └── GET /api/prices/statistics/{period}
├── Agent 3 Endpoints
│   ├── GET /api/tracking/weekly
│   ├── GET /api/tracking/monthly
│   ├── GET /api/tracking/all
│   ├── GET /api/alerts/recent
│   └── POST /api/alerts/check
└── Dashboard Endpoint
    └── GET /api/dashboard
```

### 3. Agent Layer (Multi-Agent System)

#### **Agent 1: Data Scraper & Database Manager**

**File:** `backend/agents/data_scraper_agent.py`

**Responsibilities:**
1. Scrape gold price data from external website
2. Parse HTML tables into structured data
3. Store data in database (avoiding duplicates)
4. Update existing records if needed
5. Maintain data integrity

**Key Methods:**
```python
class DataScraperAgent:
    - scrape_gold_prices()     # Async web scraping
    - parse_price()            # Convert string to float
    - parse_date()             # Convert string to date
    - get_existing_dates()     # Check duplicates
    - store_prices()           # Database operations
    - sync_data()              # Main orchestration
```

**Data Flow:**
```
Website → HTTP Request → HTML Response → BeautifulSoup Parser
→ Structured Data → Database Check → Insert/Update → Database
```

#### **Agent 2: Data Provider & Visualization Engine**

**File:** `backend/agents/data_provider_agent.py`

**Responsibilities:**
1. Query database with filters
2. Aggregate data (daily/monthly/yearly)
3. Calculate statistics
4. Format data for frontend
5. Provide multiple view modes

**Key Methods:**
```python
class DataProviderAgent:
    - get_daily_prices()           # Filter by date range
    - get_latest_price()           # Most recent record
    - get_prices_by_period()       # Period-based filter
    - get_monthly_aggregated_data() # Monthly averages
    - get_yearly_aggregated_data()  # Yearly averages
    - get_price_statistics()        # Statistical summary
```

**Aggregation Logic:**
```
Daily View:    Raw data points from database
Monthly View:  Group by year-month → Calculate averages/min/max
Yearly View:   Group by year → Calculate averages/min/max
```

#### **Agent 3: Price Tracker & Alert System**

**File:** `backend/agents/price_tracker_agent.py`

**Responsibilities:**
1. Calculate percentage changes
2. Compare current price to historical prices
3. Generate alerts based on thresholds
4. Classify alert severity
5. Store alert history

**Key Methods:**
```python
class PriceTrackerAgent:
    - calculate_percentage_change()  # Math calculation
    - get_price_change_weekly()      # 7-day comparison
    - get_price_change_monthly()     # 30-day comparison
    - get_all_price_tracking()       # Comprehensive analysis
    - check_and_generate_alerts()    # Main alert logic
    - save_alert()                   # Persist alerts
```

**Alert Logic:**
```
Current Price vs Base Price
    │
    ├─> Calculate % change
    │
    ├─> Check thresholds:
    │   ├─> Decrease ≥ 5%  → CRITICAL (Red)
    │   ├─> Increase ≥ 10% → CRITICAL (Green)
    │   └─> Other change   → INFO (Blue)
    │
    └─> Generate alert message & save to DB
```

**Thresholds:**
```python
CRITICAL_DECREASE_THRESHOLD = 5.0   # 5% drop
CRITICAL_INCREASE_THRESHOLD = 10.0  # 10% rise
```

### 4. Database Layer (SQLAlchemy + SQLite)

**File:** `backend/models/database_models.py`

#### **Table: gold_prices**
```
┌──────────────────────────────────────────┐
│ gold_prices                              │
├──────────────────┬───────────────────────┤
│ Column           │ Type                  │
├──────────────────┼───────────────────────┤
│ id               │ INTEGER (PK)          │
│ date             │ DATE (UNIQUE, INDEX)  │
│ gold_ounce       │ FLOAT                 │
│ carat_24_1gram   │ FLOAT                 │
│ carat_22_1gram   │ FLOAT                 │
│ carat_22_8grams  │ FLOAT                 │
│ carat_21_1gram   │ FLOAT                 │
│ created_at       │ DATETIME              │
│ updated_at       │ DATETIME              │
└──────────────────┴───────────────────────┘
```

#### **Table: price_alerts**
```
┌──────────────────────────────────────────┐
│ price_alerts                             │
├──────────────────┬───────────────────────┤
│ Column           │ Type                  │
├──────────────────┼───────────────────────┤
│ id               │ INTEGER (PK)          │
│ alert_type       │ STRING                │
│ percentage       │ FLOAT                 │
│ base_price       │ FLOAT                 │
│ current_price    │ FLOAT                 │
│ date_triggered   │ DATE                  │
│ period_type      │ STRING                │
│ is_critical      │ INTEGER (0/1)         │
│ created_at       │ DATETIME              │
└──────────────────┴───────────────────────┘
```

**Connection Management:**
```python
# File: backend/database/connection.py

DATABASE_URL = "sqlite:///./gold_prices.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Dependency injection for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 🔄 Data Flow Diagrams

### 1. Data Scraping Flow

```
User clicks "Sync Data"
    │
    ▼
Frontend sends POST /api/scrape/sync
    │
    ▼
FastAPI endpoint calls Agent 1
    │
    ▼
Agent 1:
    ├─> Makes HTTP request to website
    ├─> Parses HTML with BeautifulSoup
    ├─> Extracts price data from table
    ├─> Converts strings to numbers/dates
    ├─> Checks for existing records in DB
    ├─> Inserts new records
    ├─> Updates existing records
    └─> Returns result
    │
    ▼
FastAPI returns JSON response
    │
    ▼
Frontend displays success message
```

### 2. Chart Display Flow

```
User selects "3 months" period
    │
    ▼
Frontend sends GET /api/prices/period/3months
    │
    ▼
FastAPI endpoint calls Agent 2
    │
    ▼
Agent 2:
    ├─> Calculates date range (today - 90 days)
    ├─> Queries database with filters
    ├─> Converts records to dictionaries
    └─> Returns data array
    │
    ▼
FastAPI returns JSON response
    │
    ▼
Frontend:
    ├─> Updates priceData state
    ├─> Recharts re-renders
    └─> Displays updated chart
```

### 3. Alert Generation Flow

```
Dashboard loads
    │
    ▼
Frontend sends GET /api/tracking/all
    │
    ▼
FastAPI endpoint calls Agent 3
    │
    ▼
Agent 3:
    ├─> Gets latest price from DB
    ├─> Gets price from 7 days ago
    ├─> Calculates weekly % change
    ├─> Checks if critical threshold met
    ├─> Gets price from 30 days ago
    ├─> Calculates monthly % change
    ├─> Checks if critical threshold met
    ├─> Generates alert messages
    ├─> Saves critical alerts to DB
    └─> Returns comprehensive tracking data
    │
    ▼
FastAPI returns JSON response
    │
    ▼
Frontend displays alerts with color coding
```

## 🔐 Security Considerations

### Current Implementation
- CORS enabled for all origins (development mode)
- No authentication (single-user system)
- SQLite database (local file)

### Production Recommendations
1. **CORS**: Restrict to specific origins
2. **Authentication**: Add API keys or JWT
3. **Rate Limiting**: Prevent API abuse
4. **Database**: Use PostgreSQL or MySQL
5. **HTTPS**: Enable SSL/TLS
6. **Input Validation**: Already implemented with Pydantic

## ⚡ Performance Optimizations

### Current Optimizations
1. **Async Operations**: Web scraping uses AsyncIO
2. **Database Indexing**: Date column indexed
3. **Efficient Queries**: Only fetch needed columns
4. **Client-side Caching**: React state management
5. **Aggregation**: Calculated on backend, not frontend

### Potential Improvements
1. **Caching**: Add Redis for API responses
2. **Pagination**: For large datasets
3. **Background Jobs**: Schedule scraping with APScheduler
4. **Database Connection Pooling**: Already implemented
5. **Frontend Code Splitting**: Lazy load components

## 🔧 Configuration Management

### Backend Configuration
```python
# Environment variables (.env file)
DATABASE_URL = "sqlite:///./gold_prices.db"
API_HOST = "0.0.0.0"
API_PORT = 8000
```

### Frontend Configuration
```javascript
// API base URL
const API_BASE_URL = 'http://localhost:8000/api';

// Chart configuration
const periods = ['month', '3months', '6months', 'year', 'all'];
const viewModes = ['daily', 'monthly', 'yearly'];
```

## 📊 Scalability Considerations

### Current Capacity
- **Database**: SQLite handles 100K+ records easily
- **API**: FastAPI supports 1000+ requests/second
- **Frontend**: React handles large datasets with Recharts

### Scaling Strategies
1. **Horizontal**: Deploy multiple backend instances
2. **Vertical**: Increase server resources
3. **Database**: Move to PostgreSQL with read replicas
4. **Caching**: Add Redis for frequent queries
5. **CDN**: Serve frontend from CDN

## 🧪 Testing Strategy

### Unit Tests
- Test each agent independently
- Mock database operations
- Test data parsing logic

### Integration Tests
- Test API endpoints
- Test database operations
- Test agent interactions

### End-to-End Tests
- Test complete user workflows
- Test error handling
- Test edge cases

## 📈 Monitoring & Logging

### Current Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example usage
logger.info("Data synchronization complete")
logger.error(f"Error scraping website: {e}")
```

### Production Monitoring
1. **Application Logs**: Structured logging (JSON)
2. **Error Tracking**: Sentry or similar
3. **Performance**: New Relic or Datadog
4. **Uptime**: Pingdom or UptimeRobot
5. **Database**: Query performance monitoring

## 🚀 Deployment Options

### Option 1: Traditional Server
```bash
# Backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
# Serve dist/ with nginx
```

### Option 2: Docker
```dockerfile
# Backend Dockerfile
FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# Frontend Dockerfile
FROM node:18
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
```

### Option 3: Cloud Platform
- **Backend**: Railway, Render, or AWS Lambda
- **Frontend**: Vercel, Netlify, or Cloudflare Pages
- **Database**: AWS RDS, DigitalOcean, or Supabase

## 📚 Technology Decisions

### Why FastAPI?
- Automatic API documentation
- Async support for web scraping
- Type hints with Pydantic
- High performance
- Modern Python framework

### Why SQLite?
- Zero configuration
- Single file database
- Perfect for single-user systems
- Easy backup
- Good performance for this use case

### Why React?
- Component-based architecture
- Large ecosystem
- Excellent performance
- Virtual DOM
- Wide community support

### Why Recharts?
- Easy to use
- Beautiful charts
- Responsive
- TypeScript support
- Active maintenance

## 🎯 Design Patterns Used

1. **Agent Pattern**: Three independent agents
2. **Repository Pattern**: Database access layer
3. **Dependency Injection**: FastAPI's get_db()
4. **Component Pattern**: React components
5. **State Management**: React hooks
6. **API Gateway**: FastAPI as single entry point

## 🔮 Future Architecture

### Microservices Approach
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Scraper   │  │   Analytics │  │    Alert    │
│   Service   │  │   Service   │  │   Service   │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┴────────────────┘
                        │
                 ┌──────▼──────┐
                 │  API Gateway │
                 └──────┬──────┘
                        │
                 ┌──────▼──────┐
                 │   Frontend  │
                 └─────────────┘
```

### Event-Driven Architecture
```
Price Update Event → Message Queue (RabbitMQ/Kafka)
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
    ▼                     ▼                     ▼
Analytics Service    Alert Service    Notification Service
```

This architecture provides a solid foundation for a production-ready gold price analysis system while maintaining simplicity and ease of understanding.
