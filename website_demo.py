#!/usr/bin/env python3

from simple_website_tester import SimpleWebsiteTester
from utils import validate_environment
import time

def run_website_demo():
    print("🚀 Website Tester Demo")
    print("=" * 60)
    print("Testing websites without any LLM - pure automation!")
    print("=" * 60)
    
    try:
        print("🔧 Validating environment...")
        validate_environment()
        print("✅ Environment ready!")
        
        test_sites = [
            {
                "url": "https://httpbin.org",
                "name": "HTTPBin API Test Site",
                "description": "Testing API documentation site"
            },
            {
                "url": "https://example.com",
                "name": "Example.com",
                "description": "Testing basic website functionality"
            }
        ]
        
        results = []
        
        for i, site in enumerate(test_sites, 1):
            print(f"\n🧪 Test {i}/{len(test_sites)}: {site['name']}")
            print(f"🌐 URL: {site['url']}")
            print(f"📝 Description: {site['description']}")
            print("-" * 50)
            
            tester = SimpleWebsiteTester()
            success = tester.run_website_test(site['url'], f"Demo Test - {site['name']}")
            
            results.append({
                "site": site['name'],
                "url": site['url'],
                "success": success,
                "report": tester.get_test_report()
            })
            
            print(f"\n✅ Test {i} completed!")
            time.sleep(2)
        
        print("\n" + "=" * 60)
        print("📊 DEMO SUMMARY")
        print("=" * 60)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r['success'])
        
        for result in results:
            status_icon = "✅" if result['success'] else "❌"
            report = result['report']
            print(f"{status_icon} {result['site']}")
            print(f"   URL: {result['url']}")
            print(f"   Tests: {report['passed']}/{report['total_tests']} passed")
            print(f"   Status: {'PASSED' if result['success'] else 'FAILED'}")
            print()
        
        print(f"🎯 Overall Demo Result: {successful_tests}/{total_tests} sites tested successfully")
        
        if successful_tests == total_tests:
            print("🎉 All demo tests passed! Your website tester is working perfectly!")
            print("\n🚀 Ready to test any website!")
        elif successful_tests > 0:
            print("⚠️  Most demo tests passed. Some issues detected.")
        else:
            print("❌ Demo tests failed. Please check your setup.")
            
        print("\n💡 Try testing your own websites:")
        print("   python3 simple_website_tester.py https://your-site.com 'Your Test'")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    run_website_demo() 