# 🚀 Intelligent Website Tester - Web App

A modern full-stack web application that provides a beautiful SaaS-style interface for the Intelligent Website Tester. Built with FastAPI backend and React frontend.

## ✨ Features

- **🌐 Modern Web Interface** - Clean, responsive SaaS-style UI
- **⚡ Real-time Terminal Output** - Live streaming of test execution
- **📊 Interactive Results Tables** - Structured data presentation
- **🎨 Beautiful Design** - Modern UI with Tailwind CSS
- **📱 Responsive** - Works on desktop and mobile
- **🔄 WebSocket Streaming** - Real-time updates
- **📤 Export Functionality** - Copy and CSV export
- **🔒 Secure** - No API keys exposed in frontend

## 🏗️ Architecture

```
webapp/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API server
│   └── requirements.txt    # Python dependencies
└── frontend/               # React frontend
    ├── src/                # React source code
    ├── public/             # Static assets
    ├── package.json        # Node dependencies
    └── tailwind.config.js  # Tailwind configuration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Your existing `.env` file with API keys

### 1. Backend Setup

```bash
cd webapp/backend

# Install Python dependencies
pip install -r requirements.txt

# Copy your .env file from the parent directory
cp ../../.env .

# Start the backend server
python main.py
```

The backend will run on `http://localhost:8000`

### 2. Frontend Setup

```bash
cd webapp/frontend

# Install Node.js dependencies
npm install

# Start the development server
npm start
```

The frontend will run on `http://localhost:3000`

## 🎯 Usage

1. **Open the web app** at `http://localhost:3000`
2. **Enter a website URL** in the input field
3. **Click "Run Test"** to start the intelligent testing
4. **Watch real-time output** in the terminal window
5. **View structured results** in the interactive tables
6. **Export results** to CSV or copy to clipboard

## 🔧 API Endpoints

### Backend API (FastAPI)

- `POST /run-test` - Start a new website test
- `GET /test-status/{session_id}` - Get test status
- `GET /test-output/{session_id}` - Get test output
- `GET /parsed-report/{session_id}` - Get structured report
- `WS /ws/{session_id}` - WebSocket for real-time updates

### Frontend Features

- **Real-time terminal output** with WebSocket streaming
- **Interactive data tables** with status indicators
- **Export functionality** (CSV, copy to clipboard)
- **Responsive design** for all devices
- **Modern UI components** with Tailwind CSS

## 🎨 UI Components

### Terminal Output
- **Black background** with green text (classic terminal look)
- **Auto-scrolling** to latest output
- **Copy functionality** for entire output
- **Real-time streaming** via WebSocket

### Results Tables
- **Interactive tables** with sorting and filtering
- **Status badges** (PASS/FAIL/WARNING)
- **Color-coded results** for easy scanning
- **Export to CSV** functionality

### Modern Design
- **Gradient backgrounds** and modern cards
- **Responsive grid layouts**
- **Smooth animations** and transitions
- **Professional typography**

## 🚀 Deployment

### Backend Deployment (Render/Fly.io)

```bash
# For Render
# Add to render.yaml or use web interface
# Set environment variables:
# - ORGO_API_KEY
# - GOOGLE_API_KEY

# For Fly.io
fly launch
fly deploy
```

### Frontend Deployment (Vercel/Netlify)

```bash
# For Vercel
vercel

# For Netlify
netlify deploy
```

### Environment Variables

Make sure to set these in your deployment platform:

```env
ORGO_API_KEY=your_orgo_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

## 🔒 Security

- **No API keys in frontend** - All sensitive data stays in backend
- **CORS configured** for production deployment
- **Input validation** on all endpoints
- **Session management** for test isolation

## 🎯 Key Benefits

### For Users
- **No CLI knowledge required** - Beautiful web interface
- **Real-time feedback** - See tests running live
- **Professional reports** - Structured, exportable results
- **Mobile friendly** - Test from any device

### For Judges
- **Impressive demo** - Modern SaaS interface
- **Technical sophistication** - Full-stack application
- **Professional presentation** - Clean, modern design
- **Real-time capabilities** - Live streaming and updates

## 🔧 Development

### Backend Development

```bash
cd webapp/backend
pip install -r requirements.txt
python main.py
```

### Frontend Development

```bash
cd webapp/frontend
npm install
npm start
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🎉 Ready to Impress!

Your intelligent website tester now has a **professional web interface** that will wow judges and users alike!

**Features that stand out:**
- 🎨 **Modern SaaS design** like Vercel/Notion
- ⚡ **Real-time terminal output** with live streaming
- 📊 **Interactive data tables** with export functionality
- 📱 **Fully responsive** design
- 🔒 **Secure architecture** with proper separation

**Perfect for:**
- 🏆 **Hackathon demos**
- 💼 **Portfolio projects**
- 🚀 **Production deployments**
- 📈 **User demonstrations** 