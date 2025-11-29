#!/bin/bash

# Gold Price Analyzer - Startup Script
# This script starts both backend and frontend servers

echo "🚀 Starting Gold Price Analyzer Multi-Agent System"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo ""
echo "📦 Setting up Backend..."
echo "========================"

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Start backend server in background
echo "Starting FastAPI backend server on port 8000..."
python main.py &
BACKEND_PID=$!

echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 3

echo ""
echo "📦 Setting up Frontend..."
echo "========================="

# Navigate to frontend directory
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start frontend development server
echo "Starting React frontend on port 3000..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "=================================================="
echo "✅ Gold Price Analyzer is running!"
echo "=================================================="
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All servers stopped"
    exit 0
}

# Register cleanup function
trap cleanup INT TERM

# Wait for user interrupt
wait
