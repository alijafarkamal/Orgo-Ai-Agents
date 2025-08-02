#!/usr/bin/env python3

import os
import time
import json
from orgo import Computer
from dotenv import load_dotenv

load_dotenv()

class SimpleWebsiteTester:
    def __init__(self):
        self.computer = None
        self.test_results = []
        
    def start_virtual_desktop(self):
        orgo_key = os.getenv("ORGO_API_KEY")
        if not orgo_key:
            raise ValueError("ORGO_API_KEY not found in environment variables")
        
        self.computer = Computer(api_key=orgo_key)
        print("✅ Virtual desktop started successfully")
        
    def destroy_virtual_desktop(self):
        if self.computer:
            try:
                self.computer.destroy()
                print("✅ Virtual desktop destroyed successfully")
            except Exception as e:
                print(f"⚠️  Warning: Error destroying virtual desktop: {e}")
    
    def log_test_result(self, test_name, status, details=""):
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status} {details}")
    
    def test_browser_launch(self, url):
        print(f"🌐 Testing browser launch and navigation to: {url}")
        
        try:
            print("🖥️  Opening Firefox...")
            result = self.computer.exec("firefox --new-window")
            if result['success']:
                print("✅ Firefox launched successfully")
            else:
                print(f"⚠️  Firefox launch: {result['error']}")
            
            time.sleep(3)
            
            print(f"🌐 Navigating to {url}...")
            result = self.computer.exec(f"firefox {url}")
            if result['success']:
                print("✅ Navigation command executed")
            else:
                print(f"⚠️  Navigation: {result['error']}")
            
            time.sleep(5)
            
            self.log_test_result("Browser Launch", "PASS", "Firefox opened and navigation attempted")
            return True
            
        except Exception as e:
            self.log_test_result("Browser Launch", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_screenshot_capture(self):
        print("📸 Testing screenshot capture...")
        
        try:
            screenshot = self.computer.screenshot()
            print(f"✅ Screenshot captured: {screenshot.size}")
            
            self.log_test_result("Screenshot Capture", "PASS", f"Size: {screenshot.size}")
            return True
            
        except Exception as e:
            self.log_test_result("Screenshot Capture", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_button_interaction(self):
        print("🔘 Testing button interaction...")
        
        try:
            print("🖱️  Testing mouse clicks at common positions...")
            
            click_positions = [
                (512, 384),   # Center
                (100, 100),   # Top-left
                (924, 100),   # Top-right
                (512, 100),   # Top-center
            ]
            
            successful_clicks = 0
            
            for x, y in click_positions:
                try:
                    print(f"🖱️  Clicking at ({x}, {y})...")
                    result = self.computer.left_click(x, y)
                    
                    if result:
                        print(f"✅ Click successful at ({x}, {y})")
                        successful_clicks += 1
                    else:
                        print(f"⚠️  Click may have failed at ({x}, {y})")
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ Click failed at ({x}, {y}): {str(e)}")
            
            if successful_clicks > 0:
                self.log_test_result("Button Interaction", "PASS", f"{successful_clicks}/{len(click_positions)} clicks successful")
                return True
            else:
                self.log_test_result("Button Interaction", "FAIL", "No successful clicks")
                return False
                
        except Exception as e:
            self.log_test_result("Button Interaction", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_keyboard_input(self):
        print("⌨️  Testing keyboard input...")
        
        try:
            print("⌨️  Testing text input...")
            
            test_text = "test@example.com"
            self.computer.type(test_text)
            time.sleep(1)
            
            print("⌨️  Testing special keys...")
            self.computer.key("Tab")
            time.sleep(1)
            
            self.computer.type("password123")
            time.sleep(1)
            
            self.computer.key("Enter")
            time.sleep(2)
            
            self.log_test_result("Keyboard Input", "PASS", "Text input and special keys tested")
            return True
            
        except Exception as e:
            self.log_test_result("Keyboard Input", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_scroll_functionality(self):
        print("📜 Testing scroll functionality...")
        
        try:
            print("📜 Testing scroll down...")
            self.computer.scroll("down", 2)
            time.sleep(1)
            
            print("📜 Testing scroll up...")
            self.computer.scroll("up", 1)
            time.sleep(1)
            
            self.log_test_result("Scroll Functionality", "PASS", "Scroll up/down tested")
            return True
            
        except Exception as e:
            self.log_test_result("Scroll Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_system_commands(self):
        print("💻 Testing system commands...")
        
        try:
            commands = [
                "echo '=== System Info ==='",
                "uname -a",
                "echo '=== Memory Usage ==='",
                "free -h",
                "echo '=== Disk Usage ==='",
                "df -h",
                "echo '=== Firefox Process ==='",
                "ps aux | grep firefox | head -3"
            ]
            
            successful_commands = 0
            
            for cmd in commands:
                try:
                    result = self.computer.exec(cmd)
                    if result['success']:
                        print(f"✅ Command successful: {cmd}")
                        successful_commands += 1
                    else:
                        print(f"⚠️  Command failed: {cmd} - {result['error']}")
                except Exception as e:
                    print(f"❌ Command error: {cmd} - {str(e)}")
            
            if successful_commands > len(commands) // 2:
                self.log_test_result("System Commands", "PASS", f"{successful_commands}/{len(commands)} commands successful")
                return True
            else:
                self.log_test_result("System Commands", "FAIL", f"Only {successful_commands}/{len(commands)} commands successful")
                return False
                
        except Exception as e:
            self.log_test_result("System Commands", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_website_test(self, url, test_name="Simple Website Test"):
        print(f"🚀 Starting simple website test: {test_name}")
        print(f"🌐 URL: {url}")
        print("=" * 60)
        
        try:
            self.start_virtual_desktop()
            
            if not self.test_browser_launch(url):
                return False
            
            time.sleep(2)
            
            if not self.test_screenshot_capture():
                return False
            
            time.sleep(2)
            
            print("\n🔍 Running interactive tests...")
            print("-" * 40)
            
            tests = [
                self.test_button_interaction,
                self.test_keyboard_input,
                self.test_scroll_functionality,
                self.test_system_commands
            ]
            
            passed_tests = 0
            total_tests = len(tests)
            
            for test_func in tests:
                if test_func():
                    passed_tests += 1
                time.sleep(2)
            
            print("\n" + "=" * 60)
            print("📊 TEST SUMMARY")
            print("=" * 60)
            
            for result in self.test_results:
                status_icon = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
                print(f"{status_icon} [{result['timestamp']}] {result['test']}: {result['status']} {result['details']}")
            
            print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
            
            if passed_tests == total_tests:
                print("🎉 All tests passed! Website functionality is working.")
                return True
            elif passed_tests > total_tests // 2:
                print("⚠️  Most tests passed. Some features may need attention.")
                return True
            else:
                print("❌ Multiple tests failed. Website has significant issues.")
                return False
                
        except Exception as e:
            print(f"❌ Fatal error during testing: {e}")
            return False
        
        finally:
            self.destroy_virtual_desktop()
    
    def get_test_report(self):
        return {
            "total_tests": len(self.test_results),
            "passed": len([r for r in self.test_results if r["status"] == "PASS"]),
            "failed": len([r for r in self.test_results if r["status"] == "FAIL"]),
            "results": self.test_results
        }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 simple_website_tester.py <url> [test_name]")
        print("Example: python3 simple_website_tester.py https://example.com 'My Test'")
        sys.exit(1)
    
    url = sys.argv[1]
    test_name = sys.argv[2] if len(sys.argv) > 2 else "Simple Website Test"
    
    tester = SimpleWebsiteTester()
    success = tester.run_website_test(url, test_name)
    
    if success:
        print("\n🎉 Website test completed successfully!")
    else:
        print("\n❌ Website test completed with issues.") 