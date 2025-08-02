# Website Tester - No LLM Required

A comprehensive website testing tool that automatically checks buttons, forms, navigation, and other interactive elements without using any AI/LLM. Uses Orgo virtual desktops for real browser testing.

## 🚀 Features

- **No LLM Required** - Pure automation without AI
- **Real Browser Testing** - Uses actual Firefox browser
- **Interactive Testing** - Clicks buttons, types text, scrolls pages
- **Screenshot Capture** - Visual verification of each step
- **Comprehensive Reports** - Detailed pass/fail results
- **Multiple Testing Modes** - Basic and advanced options

## 📋 What It Tests

### ✅ Core Functionality
- **Browser Launch** - Firefox opens and loads websites
- **Screenshot Capture** - Visual verification of page loading
- **Button Interaction** - Clicks at common button positions
- **Keyboard Input** - Types text and uses special keys
- **Scroll Functionality** - Tests page scrolling
- **System Commands** - Verifies system responsiveness

### 🔍 Advanced Features (Advanced Mode)
- **Form Testing** - Input fields, textareas, selects
- **Navigation Testing** - Links and menus
- **Responsive Design** - Layout adaptation
- **Performance Metrics** - Memory and process monitoring
- **Accessibility** - Keyboard navigation
- **Error Handling** - Invalid URL testing

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- Orgo API Key

### Installation
```bash
pip install -r requirements.txt --break-system-packages
cp env_template.txt .env
# Add your ORGO_API_KEY to .env
```

### Basic Usage
```bash
# Simple website test
python3 simple_website_tester.py https://example.com "My Test"

# Advanced website test
python3 main_website_tester.py https://example.com --test-name "Advanced Test"

# Save detailed report
python3 main_website_tester.py https://example.com --save-report
```

## 🧪 Test Examples

### Test a Login Form
```bash
python3 simple_website_tester.py https://example.com/login "Login Form Test"
```

### Test an E-commerce Site
```bash
python3 main_website_tester.py https://shop.example.com --test-name "E-commerce Test" --save-report
```

### Test Multiple Sites
```bash
# Test multiple websites in sequence
python3 simple_website_tester.py https://google.com "Google Test"
python3 simple_website_tester.py https://github.com "GitHub Test"
python3 simple_website_tester.py https://stackoverflow.com "Stack Overflow Test"
```

## 📊 Understanding Test Results

### Test Output Example
```
🚀 Starting simple website test: HTTPBin Test
🌐 URL: https://httpbin.org
============================================================
✅ Virtual desktop started successfully
🌐 Testing browser launch and navigation to: https://httpbin.org
🖥️  Opening Firefox...
✅ Firefox launched successfully
🌐 Navigating to https://httpbin.org...
✅ Navigation command executed
✅ Browser Launch: PASS Firefox opened and navigation attempted
📸 Testing screenshot capture...
✅ Screenshot captured: (1024, 768)
✅ Screenshot Capture: PASS Size: (1024, 768)

🔍 Running interactive tests...
----------------------------------------
🔘 Testing button interaction...
🖱️  Testing mouse clicks at common positions...
🖱️  Clicking at (512, 384)...
✅ Click successful at (512, 384)
✅ Button Interaction: PASS 4/4 clicks successful
⌨️  Testing keyboard input...
✅ Keyboard Input: PASS Text input and special keys tested
📜 Testing scroll functionality...
✅ Scroll Functionality: PASS Scroll up/down tested
💻 Testing system commands...
✅ System Commands: PASS 8/8 commands successful

============================================================
📊 TEST SUMMARY
============================================================
✅ [13:33:23] Browser Launch: PASS Firefox opened and navigation attempted
✅ [13:33:29] Screenshot Capture: PASS Size: (1024, 768)
✅ [13:33:39] Button Interaction: PASS 4/4 clicks successful
✅ [13:33:50] Keyboard Input: PASS Text input and special keys tested
✅ [13:33:56] Scroll Functionality: PASS Scroll up/down tested
✅ [13:34:05] System Commands: PASS 8/8 commands successful

🎯 Overall Result: 4/4 tests passed
🎉 All tests passed! Website functionality is working.
```

### Result Interpretation

- **✅ PASS** - Test completed successfully
- **❌ FAIL** - Test failed, issue detected
- **⚠️  WARNING** - Test completed with warnings

### Overall Results
- **All tests passed** - Website is working correctly
- **Most tests passed** - Minor issues detected
- **Multiple tests failed** - Significant issues found

## 🔧 Advanced Usage

### Custom Test Scripts
```python
from simple_website_tester import SimpleWebsiteTester

# Create custom test
tester = SimpleWebsiteTester()
success = tester.run_website_test("https://example.com", "Custom Test")

if success:
    print("Website is working!")
else:
    print("Website has issues!")
```

### Batch Testing
```bash
#!/bin/bash
# test_multiple_sites.sh

sites=(
    "https://google.com"
    "https://github.com"
    "https://stackoverflow.com"
    "https://httpbin.org"
)

for site in "${sites[@]}"; do
    echo "Testing $site..."
    python3 simple_website_tester.py "$site" "Batch Test"
    echo "----------------------------------------"
done
```

## 📁 File Structure

```
qa-tester-orgo/
├── simple_website_tester.py      # ✅ WORKING - Simple website tester
├── main_website_tester.py        # ✅ WORKING - Advanced website tester
├── website_tester.py             # Basic website tester
├── advanced_website_tester.py    # Advanced website tester
├── simple_test.py               # Basic functionality test
├── requirements.txt             # Dependencies
├── .env                        # API keys
└── WEBSITE_TESTER_GUIDE.md     # This guide
```

## 🎯 Best Practices

### 1. Start Simple
```bash
# Test basic functionality first
python3 simple_website_tester.py https://example.com "Basic Test"
```

### 2. Use Descriptive Test Names
```bash
# Good test names
python3 simple_website_tester.py https://example.com/login "Login Form Test"
python3 simple_website_tester.py https://shop.example.com "E-commerce Checkout Test"
```

### 3. Save Reports for Important Tests
```bash
# Save detailed reports for critical tests
python3 main_website_tester.py https://example.com --save-report
```

### 4. Test Different Page Types
- **Home pages** - General functionality
- **Login forms** - Authentication
- **Contact forms** - User input
- **Product pages** - E-commerce functionality
- **Error pages** - Error handling

## 🔍 Troubleshooting

### Common Issues

1. **"API key required"**
   ```bash
   # Check your .env file
   cat .env
   # Should contain: ORGO_API_KEY=your_key_here
   ```

2. **"Virtual desktop failed to start"**
   - Check Orgo service status
   - Verify API key has credits
   - Ensure stable internet connection

3. **"Firefox launch failed"**
   - Virtual desktop may be overloaded
   - Try again after a few minutes
   - Check system resources

4. **"Click tests failing"**
   - Website may have different layout
   - Some sites block automated clicks
   - Normal for certain types of sites

### Debug Mode
```bash
# Test basic functionality
python3 simple_test.py

# Check environment
python3 -c "from utils import validate_environment; validate_environment()"
```

## 🚀 Ready to Use!

Your website tester is now ready! Start testing:

```bash
# Quick test
python3 simple_website_tester.py https://example.com "Quick Test"

# Comprehensive test with report
python3 main_website_tester.py https://example.com --save-report
```

**No LLM required - just pure automation!** 🎉 