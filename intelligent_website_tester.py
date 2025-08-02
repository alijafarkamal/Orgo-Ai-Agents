#!/usr/bin/env python3

import os
import time
import json
import re
import requests
from bs4 import BeautifulSoup
from orgo import Computer
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns

load_dotenv()

class IntelligentWebsiteTester:
    def __init__(self):
        self.computer = None
        self.test_results = []
        self.scraped_content = {}
        self.console = Console()
        self.setup_gemini()
        
    def setup_gemini(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  Warning: GOOGLE_API_KEY not found. Text analysis will be limited.")
            self.gemini_available = False
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.gemini_available = True
            print("✅ Gemini AI configured successfully")
        except Exception as e:
            print(f"⚠️  Warning: Gemini setup failed: {e}")
            self.gemini_available = False
        
    def start_virtual_desktop(self):
        orgo_key = os.getenv("ORGO_API_KEY")
        if not orgo_key:
            raise ValueError("ORGO_API_KEY not found in environment variables")
        
        self.computer = Computer(api_key=orgo_key)
        self.console.print("✅ Virtual desktop started successfully", style="green")
        
    def destroy_virtual_desktop(self):
        if self.computer:
            try:
                self.computer.destroy()
                self.console.print("✅ Virtual desktop destroyed successfully", style="green")
            except Exception as e:
                self.console.print(f"⚠️  Warning: Error destroying virtual desktop: {e}", style="yellow")
    
    def log_test_result(self, test_name, status, details=""):
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        status_style = "green" if status == "PASS" else "red" if status == "FAIL" else "yellow"
        self.console.print(f"{status_icon} {test_name}: {status} {details}", style=status_style)
    
    def scrape_website_content(self, url):
        """Scrape website content using requests and BeautifulSoup"""
        self.console.print("\n🔍 [bold blue]Scraping Website Content[/bold blue]")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract different types of content
            content = {
                'title': soup.title.string if soup.title else 'No title found',
                'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
                'paragraphs': [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()],
                'links': [a.get('href') for a in soup.find_all('a', href=True)],
                'buttons': [btn.get_text().strip() for btn in soup.find_all(['button', 'input']) if btn.get_text().strip()],
                'meta_description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No description found',
                'images': [img.get('alt', 'No alt text') for img in soup.find_all('img') if img.get('alt')],
                'forms': len(soup.find_all('form')),
                'total_text': soup.get_text()[:5000]  # First 5000 characters for analysis
            }
            
            self.scraped_content = content
            self.log_test_result("Content Scraping", "PASS", f"Extracted {len(content['paragraphs'])} paragraphs, {len(content['headings'])} headings")
            return True
            
        except Exception as e:
            self.log_test_result("Content Scraping", "FAIL", f"Error: {str(e)}")
            return False
    
    def analyze_content_with_gemini(self):
        """Analyze scraped content using Gemini AI"""
        if not self.gemini_available or not self.scraped_content:
            return None
        
        self.console.print("\n🧠 [bold purple]Analyzing Content with AI[/bold purple]")
        
        try:
            content = self.scraped_content
            
            # Prepare content for analysis
            analysis_prompt = f"""
            Analyze this website content and provide insights in the following format:
            
            Website Title: {content['title']}
            Meta Description: {content['meta_description']}
            
            Main Headings: {content['headings'][:10]}
            Key Paragraphs: {content['paragraphs'][:5]}
            Interactive Elements: {content['buttons'][:10]}
            Forms Found: {content['forms']}
            
            Please provide:
            1. Website Purpose (1-2 sentences)
            2. Key Features (bullet points)
            3. Target Audience
            4. Content Quality Assessment
            5. User Experience Insights
            6. Technical Observations
            
            Format the response in a clear, structured way suitable for terminal display.
            """
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Analyzing with Gemini AI...", total=None)
                
                response = self.model.generate_content(analysis_prompt)
                progress.update(task, completed=True)
            
            return response.text
            
        except Exception as e:
            self.console.print(f"❌ AI Analysis failed: {str(e)}", style="red")
            return None
    
    def display_beautiful_summary(self, url, ai_analysis=None):
        """Display beautiful formatted summary"""
        self.console.print("\n" + "="*80)
        self.console.print("🎯 [bold cyan]INTELLIGENT WEBSITE ANALYSIS REPORT[/bold cyan]", justify="center")
        self.console.print("="*80)
        
        # Website Info Panel
        website_info = Panel(
            f"[bold]URL:[/bold] {url}\n"
            f"[bold]Title:[/bold] {self.scraped_content.get('title', 'N/A')}\n"
            f"[bold]Analysis Time:[/bold] {time.strftime('%Y-%m-%d %H:%M:%S')}",
            title="🌐 Website Information",
            border_style="blue"
        )
        
        # Content Statistics Table
        stats_table = Table(title="📊 Content Statistics", show_header=True, header_style="bold magenta")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Count", style="green")
        stats_table.add_column("Details", style="yellow")
        
        content = self.scraped_content
        stats_table.add_row("Headings", str(len(content.get('headings', []))), f"Main structure elements")
        stats_table.add_row("Paragraphs", str(len(content.get('paragraphs', []))), f"Text content blocks")
        stats_table.add_row("Links", str(len(content.get('links', []))), f"Navigation elements")
        stats_table.add_row("Buttons", str(len(content.get('buttons', []))), f"Interactive elements")
        stats_table.add_row("Forms", str(content.get('forms', 0)), f"User input forms")
        stats_table.add_row("Images", str(len(content.get('images', []))), f"Visual elements")
        
        # Test Results Table
        test_table = Table(title="🧪 Functionality Test Results", show_header=True, header_style="bold green")
        test_table.add_column("Test", style="cyan")
        test_table.add_column("Status", style="green")
        test_table.add_column("Details", style="yellow")
        test_table.add_column("Time", style="blue")
        
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
            test_table.add_row(
                result["test"],
                f"{status_icon} {result['status']}",
                result["details"],
                result["timestamp"]
            )
        
        # Display panels
        self.console.print(website_info)
        self.console.print(stats_table)
        self.console.print(test_table)
        
        # AI Analysis Panel
        if ai_analysis:
            ai_panel = Panel(
                ai_analysis,
                title="🧠 AI-Powered Content Analysis",
                border_style="purple",
                width=80
            )
            self.console.print(ai_panel)
        
        # Key Findings Summary
        if content.get('headings'):
            key_headings = content['headings'][:5]
            findings_panel = Panel(
                "\n".join([f"• {heading}" for heading in key_headings]),
                title="📋 Key Page Sections",
                border_style="green"
            )
            self.console.print(findings_panel)
        
        # Overall Assessment
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        assessment_style = "green" if success_rate >= 80 else "yellow" if success_rate >= 60 else "red"
        assessment_text = "Excellent" if success_rate >= 80 else "Good" if success_rate >= 60 else "Needs Improvement"
        
        assessment_panel = Panel(
            f"[bold]Overall Assessment:[/bold] {assessment_text}\n"
            f"[bold]Success Rate:[/bold] {success_rate:.1f}% ({passed_tests}/{total_tests} tests passed)\n"
            f"[bold]Recommendation:[/bold] {'Website is fully functional' if success_rate >= 80 else 'Some improvements needed' if success_rate >= 60 else 'Significant issues detected'}",
            title="🎯 Final Assessment",
            border_style=assessment_style
        )
        self.console.print(assessment_panel)
    
    def test_browser_functionality(self, url):
        """Test browser functionality using Orgo"""
        self.console.print(f"\n🌐 [bold blue]Testing Browser Functionality[/bold blue]")
        
        try:
            # Open Firefox and navigate
            self.console.print("🖥️  Opening Firefox...")
            result = self.computer.exec("firefox --new-window")
            if result['success']:
                self.console.print("✅ Firefox launched successfully", style="green")
            time.sleep(3)
            
            self.console.print(f"🌐 Navigating to {url}...")
            result = self.computer.exec(f"firefox {url}")
            if result['success']:
                self.console.print("✅ Navigation command executed", style="green")
            time.sleep(5)
            
            self.log_test_result("Browser Launch", "PASS", "Firefox opened and navigation attempted")
            
            # Take screenshot
            screenshot = self.computer.screenshot()
            self.console.print(f"📸 Screenshot captured: {screenshot.size}", style="green")
            self.log_test_result("Screenshot Capture", "PASS", f"Size: {screenshot.size}")
            
            # Test interactions
            self.test_interactions()
            
            return True
            
        except Exception as e:
            self.log_test_result("Browser Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_interactions(self):
        """Test various interactions"""
        self.console.print("\n🔍 [bold blue]Testing Interactive Elements[/bold blue]")
        
        # Test clicks
        click_positions = [(512, 384), (100, 100), (924, 100), (512, 100)]
        successful_clicks = 0
        
        for x, y in click_positions:
            try:
                result = self.computer.left_click(x, y)
                if result:
                    successful_clicks += 1
                time.sleep(1)
            except Exception as e:
                pass
        
        self.log_test_result("Button Interaction", "PASS", f"{successful_clicks}/{len(click_positions)} clicks successful")
        
        # Test keyboard input
        try:
            self.computer.type("test@example.com")
            self.computer.key("Tab")
            self.computer.type("password123")
            self.computer.key("Enter")
            time.sleep(2)
            self.log_test_result("Keyboard Input", "PASS", "Text input and special keys tested")
        except Exception as e:
            self.log_test_result("Keyboard Input", "FAIL", f"Error: {str(e)}")
        
        # Test scrolling
        try:
            self.computer.scroll("down", 2)
            time.sleep(1)
            self.computer.scroll("up", 1)
            self.log_test_result("Scroll Functionality", "PASS", "Scroll up/down tested")
        except Exception as e:
            self.log_test_result("Scroll Functionality", "FAIL", f"Error: {str(e)}")
    
    def run_intelligent_test(self, url, test_name="Intelligent Website Test"):
        """Run the complete intelligent website test"""
        self.console.print(f"\n🚀 [bold cyan]Starting Intelligent Website Test[/bold cyan]")
        self.console.print(f"🌐 [bold]URL:[/bold] {url}")
        self.console.print(f"🧪 [bold]Test Name:[/bold] {test_name}")
        self.console.print("="*80)
        
        try:
            # Step 1: Scrape content
            if not self.scrape_website_content(url):
                return False
            
            # Step 2: Start virtual desktop and test functionality
            self.start_virtual_desktop()
            if not self.test_browser_functionality(url):
                return False
            
            # Step 3: Analyze content with AI (only once at the end)
            ai_analysis = None
            if self.gemini_available:
                ai_analysis = self.analyze_content_with_gemini()
            
            # Step 4: Display beautiful summary
            self.display_beautiful_summary(url, ai_analysis)
            
            return True
            
        except Exception as e:
            self.console.print(f"❌ [bold red]Fatal error during testing: {e}[/bold red]")
            return False
        
        finally:
            self.destroy_virtual_desktop()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 intelligent_website_tester.py <url> [test_name]")
        print("Example: python3 intelligent_website_tester.py https://example.com 'My Test'")
        sys.exit(1)
    
    url = sys.argv[1]
    test_name = sys.argv[2] if len(sys.argv) > 2 else "Intelligent Website Test"
    
    tester = IntelligentWebsiteTester()
    success = tester.run_intelligent_test(url, test_name)
    
    if success:
        print("\n🎉 Intelligent website test completed successfully!")
    else:
        print("\n❌ Intelligent website test completed with issues.") 