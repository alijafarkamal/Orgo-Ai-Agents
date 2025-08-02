# 🚀 Quick Start Guide

## 📁 Clean Project Structure (9 files only!)

```
orgo-ai-agent/
├── 🧠 intelligent_website_tester.py  # MAIN - AI-powered testing
├── ⚡ simple_website_tester.py       # SIMPLE - Basic testing (no AI)
├── 🧪 simple_test.py                 # BASIC - Functionality test
├── 🎬 website_demo.py                # DEMO - Showcase script
├── 🔧 utils.py                       # UTILS - Helper functions
├── 📦 requirements.txt               # DEPENDENCIES
├── 🔑 env_template.txt               # API KEYS TEMPLATE
├── 📖 README.md                      # FULL DOCUMENTATION
├── 📚 WEBSITE_TESTER_GUIDE.md       # DETAILED GUIDE
└── 🚀 QUICK_START.md                 # THIS FILE
```

## ⚡ 3-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt --break-system-packages
```

### 2. Set Up API Keys
```bash
cp env_template.txt .env
# Edit .env and add:
# ORGO_API_KEY=your_orgo_key_here
# GOOGLE_API_KEY=your_gemini_key_here (optional)
```

### 3. Run Tests

#### 🧠 AI-Powered Testing (Beautiful Output)
```bash
python3 intelligent_website_tester.py https://example.com "My Test"
```

#### ⚡ Simple Testing (No AI Required)
```bash
python3 simple_website_tester.py https://example.com "My Test"
```

#### 🎬 See It In Action
```bash
python3 website_demo.py
```

#### 🧪 Test Basic Functionality
```bash
python3 simple_test.py
```

## 🎯 What Each File Does

| File | Purpose | AI Required | Best For |
|------|---------|-------------|----------|
| `intelligent_website_tester.py` | 🧠 AI-powered analysis | ✅ Yes | **Main testing** |
| `simple_website_tester.py` | ⚡ Basic functionality | ❌ No | **Quick tests** |
| `simple_test.py` | 🧪 Basic verification | ❌ No | **Troubleshooting** |
| `website_demo.py` | 🎬 Showcase multiple sites | ❌ No | **Demonstrations** |

## 🎨 Beautiful Output Features

- **📊 Data Tables** - Content statistics
- **🎯 Information Panels** - Website details
- **📈 Progress Bars** - Real-time progress
- **🎨 Color-coded Results** - Green/Red status
- **📋 Professional Reports** - Structured summaries

## 🚀 Ready to Use!

**Start with the demo:**
```bash
python3 website_demo.py
```

**Then test your own websites:**
```bash
python3 intelligent_website_tester.py https://your-site.com "Your Test"
```

**No local browser required - all testing happens in the cloud!** 🌐 