# Gold Price Analyzer - Multi-Agent System

A comprehensive multi-agent system for analyzing gold prices in Sri Lanka with real-time scraping, intelligent tracking, and beautiful visualization.

## 🏗️ Architecture Overview

This system consists of **3 intelligent agents** working together:

### **Agent 1: Data Scraper & Database Manager**
- Scrapes gold price data from https://www.ideabeam.com/finance/rates/goldprice.php
- Automatically updates database with missing values
- Prevents duplicate entries
- Maintains complete historical data

### **Agent 2: Data Provider & Visualization Engine**
- Provides filtered data for different time periods (1 month, 3 months, 6 months, 1 year, all time)
- Supports multiple view modes (daily, monthly, yearly aggregates)
- Generates statistical summaries
- Powers the frontend dashboard

### **Agent 3: Price Tracker & Alert System**
- Monitors weekly and monthly price changes
- **Critical Alert:** Triggers when price decreases by 5% or more
- **Critical Alert:** Triggers when price increases by 10% or more
- Shows percentage changes for all periods
- Stores alert history in database

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database
- **BeautifulSoup4** - Web scraping
- **httpx** - Async HTTP client

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database and start server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🚀 Usage

### First Time Setup

1. Start the backend server
2. Start the frontend development server
3. Open `http://localhost:3000` in your browser
4. Click **"Sync Data"** button to perform initial data scraping

### Features

#### 📊 Dashboard
- **Current Prices**: Real-time display of gold prices for different carats
- **Price History Chart**: Interactive chart with customizable periods
- **View Modes**: Switch between daily, monthly, and yearly aggregations
- **Statistics**: Min, max, average prices with percentage changes

#### 🔔 Alerts
- **Critical Alerts**: Highlighted when thresholds are exceeded
  - Red alert: Price decreased ≥ 5%
  - Green alert: Price increased ≥ 10%
- **Info Alerts**: Shows all percentage changes for tracking

#### 📈 Chart Controls
- **Time Periods**: 1 month, 3 months, 6 months, 1 year, all time
- **View Modes**: Daily data points, monthly averages, yearly averages
- **Interactive**: Hover over chart for detailed information

## 📡 API Endpoints

### Agent 1: Data Scraper
- `POST /api/scrape/sync` - Trigger data synchronization
- `GET /api/scrape/status` - Get scraper status

### Agent 2: Data Provider
- `GET /api/prices/latest` - Get most recent price
- `GET /api/prices/period/{period}` - Get prices for period (month, 3months, 6months, year, all)
- `GET /api/prices/monthly-aggregate` - Get monthly aggregated data
- `GET /api/prices/yearly-aggregate` - Get yearly aggregated data
- `GET /api/prices/statistics/{period}` - Get statistical summary

### Agent 3: Price Tracker
- `GET /api/tracking/weekly` - Get weekly price tracking
- `GET /api/tracking/monthly` - Get monthly price tracking
- `GET /api/tracking/all` - Get comprehensive tracking with alerts
- `GET /api/alerts/recent` - Get recent alerts
- `POST /api/alerts/check` - Manually trigger alert checking

### Dashboard
- `GET /api/dashboard` - Get all dashboard data in one request

## 📁 Project Structure

```
gold-price-analyzer/
├── backend/
│   ├── agents/
│   │   ├── data_scraper_agent.py      # Agent 1
│   │   ├── data_provider_agent.py     # Agent 2
│   │   └── price_tracker_agent.py     # Agent 3
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   └── database_models.py
│   ├── main.py                        # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── GoldPriceAnalyzer.jsx     # Main component
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
└── README.md
```

## 🔄 Data Flow

1. **User triggers sync** → Agent 1 scrapes website → Stores/updates database
2. **User selects period** → Agent 2 queries database → Returns filtered data
3. **Frontend displays chart** → User interacts with controls → Chart updates
4. **Agent 3 monitors prices** → Calculates changes → Generates alerts
5. **Dashboard loads** → Combines all agent data → Shows comprehensive view

## 🎯 Key Features

### Multi-Agent Architecture
- **Separation of Concerns**: Each agent has a specific responsibility
- **Modularity**: Agents can be updated independently
- **Scalability**: Easy to add new agents or features

### Smart Data Management
- **Incremental Updates**: Only fetches new data, updates existing
- **No Duplicates**: Prevents duplicate entries in database
- **Historical Tracking**: Maintains complete price history

### Intelligent Alerting
- **Threshold-Based**: Automatic alerts at critical levels
- **Multi-Period**: Tracks both weekly and monthly changes
- **Visual Indicators**: Color-coded alerts with icons

### Responsive Design
- **Mobile-Friendly**: Works on all device sizes
- **Modern UI**: Beautiful gradient design with Tailwind CSS
- **Interactive Charts**: Powered by Recharts library

## 🔧 Configuration

### Backend
Edit `backend/.env` (create if doesn't exist):
```env
DATABASE_URL=sqlite:///./gold_prices.db
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend
The API base URL is configured in `GoldPriceAnalyzer.jsx`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## 🧪 Testing

### Test Backend Endpoints
```bash
# Health check
curl http://localhost:8000/

# Sync data
curl -X POST http://localhost:8000/api/scrape/sync

# Get latest price
curl http://localhost:8000/api/prices/latest

# Get tracking
curl http://localhost:8000/api/tracking/all
```

### Access API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 📊 Database Schema

### GoldPrice Table
- `id`: Primary key
- `date`: Unique date of record
- `gold_ounce`: Price per ounce
- `carat_24_1gram`: 24 carat 1 gram price
- `carat_22_1gram`: 22 carat 1 gram price
- `carat_22_8grams`: 22 carat 8 grams price
- `carat_21_1gram`: 21 carat 1 gram price
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp

### PriceAlert Table
- `id`: Primary key
- `alert_type`: 'increase' or 'decrease'
- `percentage`: Percentage change
- `base_price`: Starting price
- `current_price`: Current price
- `date_triggered`: Date of alert
- `period_type`: 'week' or 'month'
- `is_critical`: Boolean flag for critical alerts
- `created_at`: Alert creation timestamp

## 🚨 Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `main.py`
- **Database errors**: Delete `gold_prices.db` and restart
- **Import errors**: Ensure virtual environment is activated

### Frontend Issues
- **API connection failed**: Check if backend is running on port 8000
- **Chart not displaying**: Check browser console for errors
- **Styling issues**: Run `npm install` again

## 🔮 Future Enhancements

- [ ] Email/SMS notifications for critical alerts
- [ ] Price prediction using machine learning
- [ ] Compare with international gold prices
- [ ] Export data to CSV/Excel
- [ ] User authentication and personalized alerts
- [ ] Real-time WebSocket updates
- [ ] Mobile app (React Native)

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Built with ❤️ by a Senior AI Engineer with 25 years of experience

## 🙏 Acknowledgments

- Data source: https://www.ideabeam.com/finance/rates/goldprice.php
- FastAPI framework
- React and Recharts libraries
