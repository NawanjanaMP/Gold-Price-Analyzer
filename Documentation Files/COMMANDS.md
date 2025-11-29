# 🛠️ Command Reference - Gold Price Analyzer

## 📥 Installation Commands

### Initial Setup
```bash
# Clone or download project
cd gold-price-analyzer

# Make scripts executable
chmod +x start.sh
chmod +x test_agents.py
```

### Backend Dependencies
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Upgrade pip (optional)
pip install --upgrade pip
```

### Frontend Dependencies
```bash
cd frontend

# Install Node.js packages
npm install

# Or using yarn
yarn install

# Clear cache and reinstall (if issues)
rm -rf node_modules package-lock.json
npm install
```

## 🚀 Running Commands

### Start Everything (Recommended)
```bash
# From project root
./start.sh
```

### Backend Only
```bash
cd backend
source venv/bin/activate  # Activate venv first
python main.py

# Or with custom port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production mode
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Only
```bash
cd frontend

# Development mode
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🧪 Testing Commands

### Test All Agents
```bash
# From project root
python3 test_agents.py

# Or from backend directory
cd backend
source venv/bin/activate
python ../test_agents.py
```

### Test Individual Components
```bash
# Test Agent 1 (Data Scraper)
python -c "from agents.data_scraper_agent import DataScraperAgent; print('Agent 1 OK')"

# Test Agent 2 (Data Provider)
python -c "from agents.data_provider_agent import DataProviderAgent; print('Agent 2 OK')"

# Test Agent 3 (Price Tracker)
python -c "from agents.price_tracker_agent import PriceTrackerAgent; print('Agent 3 OK')"

# Test Database Connection
python -c "from database.connection import init_db; init_db(); print('Database OK')"
```

### API Testing with cURL
```bash
# Health check
curl http://localhost:8000/

# Sync data
curl -X POST http://localhost:8000/api/scrape/sync

# Get latest price
curl http://localhost:8000/api/prices/latest

# Get 3-month data
curl http://localhost:8000/api/prices/period/3months

# Get monthly aggregate
curl http://localhost:8000/api/prices/monthly-aggregate

# Get yearly aggregate
curl http://localhost:8000/api/prices/yearly-aggregate

# Get statistics
curl http://localhost:8000/api/prices/statistics/month

# Get weekly tracking
curl http://localhost:8000/api/tracking/weekly

# Get all tracking
curl http://localhost:8000/api/tracking/all

# Get dashboard data
curl http://localhost:8000/api/dashboard

# Pretty print JSON (Linux/Mac)
curl http://localhost:8000/api/prices/latest | python -m json.tool

# Save response to file
curl http://localhost:8000/api/prices/latest > latest_price.json
```

### API Testing with httpie (Alternative)
```bash
# Install httpie
pip install httpie

# GET requests
http GET http://localhost:8000/api/prices/latest

# POST requests
http POST http://localhost:8000/api/scrape/sync
```

## 🔍 Debugging Commands

### Check Running Processes
```bash
# Check if backend is running
lsof -i :8000
ps aux | grep python | grep main.py

# Check if frontend is running
lsof -i :3000
ps aux | grep node | grep vite
```

### View Logs
```bash
# Backend logs (if running with start.sh)
tail -f backend.log

# Frontend logs
tail -f frontend.log

# Real-time Python logging
cd backend
python main.py 2>&1 | tee app.log
```

### Database Commands
```bash
cd backend

# Open SQLite database
sqlite3 gold_prices.db

# In SQLite shell:
.tables                          # List tables
.schema gold_prices              # Show table structure
SELECT COUNT(*) FROM gold_prices;  # Count records
SELECT * FROM gold_prices ORDER BY date DESC LIMIT 5;  # Latest 5 records
SELECT * FROM price_alerts;      # View alerts
.quit                            # Exit
```

## 🧹 Cleanup Commands

### Stop Servers
```bash
# Find and kill backend process
lsof -ti :8000 | xargs kill -9

# Find and kill frontend process
lsof -ti :3000 | xargs kill -9

# Kill by process name
pkill -f "python main.py"
pkill -f "vite"

# Graceful shutdown (Ctrl+C in terminal)
```

### Clean Database
```bash
cd backend

# Delete database
rm gold_prices.db

# Database will be recreated on next run
```

### Clean Build Files
```bash
# Backend
cd backend
rm -rf __pycache__
rm -rf */__pycache__
rm -rf *.pyc
rm gold_prices.db
rm test_gold_prices.db

# Frontend
cd frontend
rm -rf node_modules
rm -rf dist
rm package-lock.json
```

### Full Clean
```bash
# From project root
cd backend
rm -rf venv __pycache__ */__pycache__ *.db

cd ../frontend
rm -rf node_modules dist package-lock.json

# Then reinstall everything
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install
```

## 📦 Build Commands

### Backend Production Build
```bash
cd backend

# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Production Build
```bash
cd frontend

# Build
npm run build

# Output will be in dist/ folder
ls -la dist/

# Preview build locally
npm run preview

# Serve with simple HTTP server
npx serve dist -l 3000
```

## 🐳 Docker Commands (Future)

### Build Docker Images
```bash
# Backend
cd backend
docker build -t gold-analyzer-backend .

# Frontend
cd frontend
docker build -t gold-analyzer-frontend .
```

### Run with Docker Compose
```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🔧 Development Commands

### Python Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows Git Bash)
source venv/Scripts/activate

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Deactivate
deactivate

# Remove venv
rm -rf venv
```

### Package Management
```bash
# Backend - Freeze dependencies
cd backend
pip freeze > requirements.txt

# Frontend - Update package.json
cd frontend
npm update

# Check for outdated packages
npm outdated
```

### Code Quality
```bash
# Python - Format with black
cd backend
pip install black
black .

# Python - Lint with flake8
pip install flake8
flake8 .

# JavaScript - Format with prettier
cd frontend
npx prettier --write "src/**/*.{js,jsx}"

# JavaScript - Lint with ESLint
npx eslint src/
```

## 📊 Monitoring Commands

### System Resources
```bash
# Check memory usage
free -h

# Check disk usage
df -h

# Check CPU usage
top
htop  # More detailed

# Monitor specific process
top -p $(pgrep -f "python main.py")
```

### Network
```bash
# Check open ports
netstat -tuln | grep 8000
netstat -tuln | grep 3000

# Test connectivity
curl -I http://localhost:8000
curl -I http://localhost:3000

# Check API response time
time curl http://localhost:8000/api/prices/latest
```

## 🔐 Security Commands

### Environment Variables
```bash
# Create .env file
cd backend
cp .env.example .env

# Edit .env
nano .env
# or
vim .env

# Load environment variables
export $(cat .env | xargs)
```

### SSL/HTTPS (Production)
```bash
# Generate self-signed certificate (testing only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Run backend with HTTPS
uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

## 📈 Performance Commands

### Benchmark API
```bash
# Install Apache Bench
sudo apt-get install apache2-utils  # Ubuntu
brew install httpd  # Mac

# Test endpoint
ab -n 1000 -c 10 http://localhost:8000/api/prices/latest

# Load test with wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/prices/latest
```

### Database Optimization
```bash
# SQLite analyze (optimize queries)
sqlite3 gold_prices.db "ANALYZE;"

# Vacuum database (reclaim space)
sqlite3 gold_prices.db "VACUUM;"

# Check database size
ls -lh gold_prices.db
```

## 🚨 Troubleshooting Commands

### Permission Issues
```bash
# Fix file permissions
chmod +x start.sh
chmod +x test_agents.py

# Fix directory permissions
chmod -R 755 backend/
chmod -R 755 frontend/
```

### Port Conflicts
```bash
# Find what's using port 8000
lsof -i :8000
sudo lsof -i :8000

# Kill process on port
kill $(lsof -t -i:8000)

# Find all Python processes
ps aux | grep python

# Find all Node processes
ps aux | grep node
```

### Module Not Found
```bash
# Reinstall Python packages
cd backend
pip install --force-reinstall -r requirements.txt

# Reinstall Node packages
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📝 Git Commands (Version Control)

### Initialize Repository
```bash
# From project root
git init
git add .
git commit -m "Initial commit: Gold Price Analyzer multi-agent system"
```

### Common Git Operations
```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Add feature: monthly view"

# View history
git log --oneline

# Create branch
git checkout -b feature/new-feature

# Push to remote
git push origin main
```

## 🎯 Quick Reference

### Most Used Commands
```bash
# Start application
./start.sh

# Test agents
python3 test_agents.py

# Backend only
cd backend && python main.py

# Frontend only
cd frontend && npm run dev

# API docs
open http://localhost:8000/docs

# Application
open http://localhost:3000

# Stop servers
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9

# Clean database
cd backend && rm *.db
```

### Environment Check
```bash
# Check Python version
python3 --version

# Check Node version
node --version
npm --version

# Check pip
pip --version

# Check installed packages
pip list
npm list --depth=0
```

---

Keep this file handy for quick reference! 🚀
