# 🚀 Quick Start Guide - Gold Price Analyzer

## ⚡ 5-Minute Setup

### Step 1: Test the Agents (Optional but Recommended)
```bash
cd gold-price-analyzer
python3 test_agents.py
```

This will:
- Create a test database
- Scrape live data from the website
- Test all 3 agents
- Show you sample output

### Step 2: Start Everything
```bash
./start.sh
```

This single command will:
1. Create Python virtual environment (if needed)
2. Install all Python dependencies
3. Start FastAPI backend on port 8000
4. Install all Node.js dependencies
5. Start React frontend on port 3000

### Step 3: Open Your Browser
```
http://localhost:3000
```

### Step 4: Sync Data
Click the "Sync Data" button in the top-right corner to populate the database with gold price data.

## 🎯 What You'll See

### Dashboard Components

1. **Header Section**
   - Application title
   - Sync Data button (use this to update prices)

2. **Current Gold Prices**
   - 4 cards showing different carat prices
   - Updates when you sync data

3. **Price Alerts** (if any thresholds are met)
   - Red alerts: Price dropped ≥ 5%
   - Green alerts: Price increased ≥ 10%
   - Blue alerts: Normal changes

4. **Interactive Chart**
   - Period buttons: 1 Month, 3 Months, 6 Months, 1 Year, All Time
   - View mode buttons: Daily, Monthly, Yearly
   - Hover over chart for details

5. **Statistics**
   - Current, Average, Min, Max prices
   - Total change in selected period

## 🔧 Manual Setup (Alternative)

If the automatic script doesn't work, follow these steps:

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

## 📊 Understanding the Agents

### Agent 1: Data Scraper
**What it does:**
- Visits https://www.ideabeam.com/finance/rates/goldprice.php
- Extracts all historical gold price data
- Stores it in SQLite database
- Only adds new data (no duplicates)

**When to use:**
- Click "Sync Data" button
- Or call: `POST /api/scrape/sync`

### Agent 2: Data Provider
**What it does:**
- Retrieves data from database
- Filters by time period
- Calculates aggregates (monthly/yearly averages)
- Provides statistics

**Automatic:**
- Runs when you select period buttons
- Runs when you change view modes
- Powers all charts and displays

### Agent 3: Price Tracker
**What it does:**
- Monitors price changes
- Compares current price to:
  * 7 days ago (weekly tracking)
  * 30 days ago (monthly tracking)
- Generates alerts when:
  * Price drops ≥ 5% (CRITICAL)
  * Price rises ≥ 10% (CRITICAL)
  * Any other change (INFO)

**Automatic:**
- Runs when dashboard loads
- Can manually trigger: `POST /api/alerts/check`

## 🎨 Customization

### Change Alert Thresholds
Edit `backend/agents/price_tracker_agent.py`:
```python
CRITICAL_DECREASE_THRESHOLD = 5.0  # Change this
CRITICAL_INCREASE_THRESHOLD = 10.0 # Change this
```

### Change Port Numbers
Backend (edit `backend/main.py`):
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000
```

Frontend (edit `frontend/vite.config.js`):
```javascript
server: {
  port: 3000,  // Change 3000
}
```

### Change Colors
Edit `frontend/src/GoldPriceAnalyzer.jsx` - look for Tailwind classes:
- `bg-amber-600` (amber background)
- `text-yellow-600` (yellow text)
- etc.

## 🐛 Common Issues

### Port Already in Use
```bash
# Find and kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Database Locked
```bash
# Delete and recreate database
cd backend
rm gold_prices.db
python main.py  # Will recreate automatically
```

### Frontend Won't Start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### No Data Showing
1. Make sure backend is running: check http://localhost:8000
2. Click "Sync Data" button
3. Check browser console for errors (F12)

## 📱 API Testing

### Using cURL
```bash
# Test API health
curl http://localhost:8000/

# Sync data
curl -X POST http://localhost:8000/api/scrape/sync

# Get latest price
curl http://localhost:8000/api/prices/latest

# Get 3-month data
curl http://localhost:8000/api/prices/period/3months

# Get tracking
curl http://localhost:8000/api/tracking/all
```

### Using Browser
Visit http://localhost:8000/docs for interactive API documentation

## 🎓 Learn More

### Understanding Multi-Agent Systems
Each agent is independent but works together:
- **Agent 1** = Data collector (fills the database)
- **Agent 2** = Data processor (serves the frontend)
- **Agent 3** = Data analyzer (creates insights)

### Database Schema
- **gold_prices** table: Historical price data
- **price_alerts** table: Generated alerts

### Frontend Architecture
- React component-based
- Recharts for visualization
- Tailwind CSS for styling
- Fetches data from FastAPI backend

## 💡 Tips

1. **First time?** Click "Sync Data" to populate database
2. **Data stale?** Click "Sync Data" to update
3. **Want historical view?** Select "All Time" period
4. **Want trends?** Switch to "Monthly" or "Yearly" view
5. **Track changes?** Watch the alerts section

## 🆘 Need Help?

Check the full README.md for detailed documentation, or:
1. Check backend logs in the terminal
2. Check frontend console (F12 in browser)
3. Visit API docs: http://localhost:8000/docs
