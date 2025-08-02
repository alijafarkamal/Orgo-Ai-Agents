# 🚀 Intelligent Website Tester with Orgo

A powerful website testing tool that combines **virtual desktop automation** with **intelligent content analysis** using Gemini AI. No LLM required for basic functionality, but AI-powered insights for comprehensive analysis.

## ✨ Features

- **🌐 Virtual Desktop Testing** - Uses Orgo to test websites in isolated cloud environments
- **🔍 Content Scraping** - Extracts and analyzes website content
- **🧠 AI-Powered Analysis** - Gemini AI provides intelligent insights about website content
- **🎨 Beautiful Terminal Output** - Rich formatting with tables, panels, and progress bars
- **📊 Comprehensive Reports** - Detailed test results with statistics and recommendations
- **⚡ No Local Browser** - All testing happens on remote virtual desktops

## 📁 Clean Project Structure

```
orgo-ai-agent/
├── intelligent_website_tester.py  # 🧠 MAIN - AI-powered website tester
├── simple_website_tester.py       # ⚡ SIMPLE - Basic website tester (no AI)
├── simple_test.py                 # 🧪 BASIC - Simple functionality test
├── website_demo.py                # 🎬 DEMO - Showcase multiple websites
├── utils.py                       # 🔧 UTILS - Helper functions
├── requirements.txt               # 📦 DEPENDENCIES
├── env_template.txt               # 🔑 API KEYS TEMPLATE
├── README.md                      # 📖 THIS FILE
└── WEBSITE_TESTER_GUIDE.md       # 📚 DETAILED GUIDE
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt --break-system-packages
```

### 2. Set Up API Keys
```bash
cp env_template.txt .env
# Edit .env and add your API keys:
# ORGO_API_KEY=your_orgo_key_here
# GOOGLE_API_KEY=your_gemini_key_here (optional for AI features)
```

### 3. Run Tests

#### 🧠 Intelligent Testing (with AI analysis)
```bash
python3 intelligent_website_tester.py https://example.com "My Test"
```

#### ⚡ Simple Testing (no AI required)
```bash
python3 simple_website_tester.py https://example.com "My Test"
```

#### 🎬 Demo Mode
```bash
python3 website_demo.py
```

#### 🧪 Basic Functionality Test
```bash
python3 simple_test.py
```

## 🎯 What Each File Does

### 🧠 `intelligent_website_tester.py` - **MAIN FILE**
- **AI-powered content analysis** using Gemini
- **Beautiful terminal output** with Rich library
- **Content scraping** and intelligent insights
- **Comprehensive testing** with detailed reports
- **Requires**: ORGO_API_KEY + GOOGLE_API_KEY

### ⚡ `simple_website_tester.py` - **SIMPLE VERSION**
- **Basic website testing** without AI
- **Virtual desktop automation** with Orgo
- **Screenshot capture** and interaction testing
- **Requires**: Only ORGO_API_KEY

### 🧪 `simple_test.py` - **BASIC TEST**
- **Quick functionality verification**
- **Tests Orgo connection** and basic features
- **Good for troubleshooting**

### 🎬 `website_demo.py` - **DEMO SCRIPT**
- **Showcases multiple websites**
- **Pre-configured test scenarios**
- **Perfect for demonstrations**

### 🔧 `utils.py` - **HELPER FUNCTIONS**
- **Environment validation**
- **Test reporting utilities**
- **Common test prompts**

## 🎨 Beautiful Output Example

The intelligent tester provides stunning terminal output with:

- **📊 Data Tables** - Content statistics and test results
- **🎯 Information Panels** - Website details and AI insights
- **📈 Progress Bars** - Real-time testing progress
- **🎨 Color-coded Results** - Green for pass, red for fail
- **📋 Structured Reports** - Professional test summaries

## 🔑 API Keys Required

### Required
- **ORGO_API_KEY** - For virtual desktop functionality

### Optional (for AI features)
- **GOOGLE_API_KEY** - For Gemini AI content analysis

## 🎯 Use Cases

### 🧠 Intelligent Testing
```bash
# Full AI-powered analysis
python3 intelligent_website_tester.py https://shop.example.com "E-commerce Test"
```

### ⚡ Quick Testing
```bash
# Basic functionality testing
python3 simple_website_tester.py https://example.com "Quick Test"
```

### 🎬 Demonstrations
```bash
# Showcase multiple sites
python3 website_demo.py
```

## 🛠️ Troubleshooting

### Common Issues
1. **API Key Errors** - Check your `.env` file
2. **Import Errors** - Run `pip install -r requirements.txt --break-system-packages`
3. **Virtual Desktop Issues** - Verify Orgo service status

### Debug Mode
```bash
# Test basic functionality
python3 simple_test.py

# Check environment
python3 -c "from utils import validate_environment; validate_environment()"
```

## 🎉 Ready to Use!

Your intelligent website tester is now ready! Start with:

```bash
# 🧠 AI-powered testing
python3 intelligent_website_tester.py https://example.com "My Test"

# ⚡ Simple testing
python3 simple_website_tester.py https://example.com "My Test"

# 🎬 See it in action
python3 website_demo.py
```

**No local browser required - all testing happens in the cloud!** 🚀 