#!/bin/bash

# Smart City Transportation System - Quick Start Script

echo "======================================"
echo "Smart City Transportation System Setup"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js/npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "✅ Project Root: $PROJECT_ROOT"
echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd "$PROJECT_ROOT/backend" || exit 1

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if ! pip show flask &> /dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Backend dependencies installed"
echo ""

# Setup Frontend
echo "📦 Setting up Frontend..."
cd "$PROJECT_ROOT" || exit 1

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo "✅ Frontend dependencies installed"
echo ""

# Summary
echo "======================================"
echo "Setup Complete! ✅"
echo "======================================"
echo ""
echo "To start the system, run in separate terminals:"
echo ""
echo "🚀 Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "🚀 Frontend (Terminal 2):"
echo "   npm start"
echo ""
echo "Then open http://localhost:4200 in your browser"
echo ""
echo "Backend API: http://localhost:5000"
echo "WebSocket: ws://localhost:5000"
echo ""
