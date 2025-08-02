import os
from orgo import Computer
from dotenv import load_dotenv

load_dotenv()

def simple_desktop_test():
    print("🧪 Running Simple Desktop Test")
    
    try:
        computer = Computer(api_key=os.getenv("ORGO_API_KEY"))
        print("✅ Virtual desktop created successfully")
        
        print("📸 Taking a screenshot...")
        screenshot = computer.screenshot()
        print(f"✅ Screenshot captured: {screenshot.size}")
        
        print("🖥️  Getting computer status...")
        status = computer.status()
        print(f"✅ Computer status: {status}")
        
        print("🧹 Destroying virtual desktop...")
        computer.destroy()
        print("✅ Virtual desktop destroyed successfully")
        
        print("🎉 Simple test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False

if __name__ == "__main__":
    simple_desktop_test() 