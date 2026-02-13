#!/bin/bash

echo "🚀 Setting up Multi-Agent Code Generator Web Interface..."
echo ""

# Check if main.py exists in parent directory
if [ ! -f "../main.py" ]; then
    echo "⚠️  Warning: main.py not found in parent directory"
    echo "Please ensure main.py and orchestrator/ are in the parent directory"
    echo "or update the path in backend/server.js (line 24)"
    echo ""
fi

# Check if orchestrator exists
if [ ! -d "../orchestrator" ]; then
  echo "❌ orchestrator folder not found in parent directory"
  exit 1
fi

echo "✅ main.py and orchestrator found"
# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
npm install
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Terminal 1: cd backend && npm start"
echo "  2. Terminal 2: cd frontend && npm run dev"
echo "  3. Open http://localhost:3000 in your browser"
echo ""
