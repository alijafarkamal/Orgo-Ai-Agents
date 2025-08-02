#!/bin/bash

echo "🎨 Setting up Intelligent Website Tester Frontend"
echo "================================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    echo "Please install npm (comes with Node.js)"
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo ""
echo "✅ Frontend setup complete!"
echo "🚀 Run 'npm start' to start the development server"
echo "🌐 The app will be available at http://localhost:3000" 