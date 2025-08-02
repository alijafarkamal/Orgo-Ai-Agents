from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess
import asyncio
import json
import re
import uuid
from typing import Dict, List, Optional
import os
import sys
from pathlib import Path

# Add parent directory to path to import the tester
sys.path.append(str(Path(__file__).parent.parent.parent))
from intelligent_website_tester import IntelligentWebsiteTester

app = FastAPI(
    title="Intelligent Website Tester API",
    description="AI-powered website testing with Orgo virtual desktops",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active test sessions
active_sessions: Dict[str, Dict] = {}

class TestRequest(BaseModel):
    url: str
    test_name: str = "Web Test"

class TestResponse(BaseModel):
    session_id: str
    status: str
    message: str

@app.get("/")
async def root():
    return {"message": "Intelligent Website Tester API", "status": "running"}

@app.post("/run-test", response_model=TestResponse)
async def run_test(request: TestRequest):
    """Start a new website test"""
    session_id = str(uuid.uuid4())
    
    # Validate URL
    if not request.url.startswith(('http://', 'https://')):
        request.url = 'https://' + request.url
    
    # Initialize session
    active_sessions[session_id] = {
        "status": "starting",
        "url": request.url,
        "test_name": request.test_name,
        "output": [],
        "results": {},
        "completed": False
    }
    
    # Start test in background
    asyncio.create_task(run_test_background(session_id, request.url, request.test_name))
    
    return TestResponse(
        session_id=session_id,
        status="started",
        message="Test started successfully"
    )

async def run_test_background(session_id: str, url: str, test_name: str):
    """Run the test in background and capture output"""
    try:
        session = active_sessions[session_id]
        session["status"] = "running"
        
        # Create a custom output capture class
        class OutputCapture:
            def __init__(self, session_id: str):
                self.session_id = session_id
                self.output_buffer = []
            
            def write(self, text: str):
                if text.strip():
                    self.output_buffer.append(text.strip())
                    # Send to WebSocket if connected
                    asyncio.create_task(broadcast_output(self.session_id, text))
            
            def flush(self):
                pass
        
        # Capture stdout
        import io
        import contextlib
        
        # Run the test with output capture
        tester = IntelligentWebsiteTester()
        
        # Override the console print method to capture output
        original_print = tester.console.print
        
        def capture_print(*args, **kwargs):
            # Convert Rich objects to plain text
            text = " ".join(str(arg) for arg in args)
            session["output"].append(text)
            asyncio.create_task(broadcast_output(session_id, text))
            original_print(*args, **kwargs)
        
        tester.console.print = capture_print
        
        # Run the test
        success = tester.run_intelligent_test(url, test_name)
        
        # Store results
        session["results"] = {
            "success": success,
            "test_results": tester.test_results,
            "scraped_content": tester.scraped_content,
            "report": tester.get_test_report()
        }
        
        session["status"] = "completed" if success else "failed"
        session["completed"] = True
        
        # Send completion message
        completion_msg = f"\n🎉 Test {'completed successfully' if success else 'completed with issues'}"
        session["output"].append(completion_msg)
        asyncio.create_task(broadcast_output(session_id, completion_msg))
        
    except Exception as e:
        session = active_sessions.get(session_id, {})
        session["status"] = "error"
        session["error"] = str(e)
        error_msg = f"\n❌ Error: {str(e)}"
        session["output"].append(error_msg)
        asyncio.create_task(broadcast_output(session_id, error_msg))

@app.get("/test-status/{session_id}")
async def get_test_status(session_id: str):
    """Get the current status of a test"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Test session not found")
    
    session = active_sessions[session_id]
    return {
        "session_id": session_id,
        "status": session["status"],
        "url": session["url"],
        "test_name": session["test_name"],
        "completed": session.get("completed", False),
        "output_count": len(session.get("output", [])),
        "results": session.get("results", {})
    }

@app.get("/test-output/{session_id}")
async def get_test_output(session_id: str):
    """Get all output for a test session"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Test session not found")
    
    session = active_sessions[session_id]
    return {
        "session_id": session_id,
        "output": session.get("output", []),
        "status": session["status"]
    }

@app.get("/parsed-report/{session_id}")
async def get_parsed_report(session_id: str):
    """Get structured report data"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Test session not found")
    
    session = active_sessions[session_id]
    if not session.get("completed", False):
        raise HTTPException(status_code=400, detail="Test not completed yet")
    
    results = session.get("results", {})
    
    # Parse the output to extract structured data
    structured_data = parse_output_to_structured(session.get("output", []))
    
    return {
        "session_id": session_id,
        "structured_data": structured_data,
        "test_results": results.get("test_results", []),
        "scraped_content": results.get("scraped_content", {}),
        "report": results.get("report", {})
    }

def parse_output_to_structured(output_lines: List[str]) -> Dict:
    """Parse the output lines to extract structured data"""
    structured = {
        "website_info": {},
        "content_statistics": {},
        "test_results": [],
        "ai_analysis": "",
        "final_assessment": {}
    }
    
    current_section = None
    ai_analysis_lines = []
    
    for line in output_lines:
        line = line.strip()
        
        # Parse website information
        if "URL:" in line:
            structured["website_info"]["url"] = line.split("URL:")[1].strip()
        elif "Title:" in line:
            structured["website_info"]["title"] = line.split("Title:")[1].strip()
        elif "Analysis Time:" in line:
            structured["website_info"]["analysis_time"] = line.split("Analysis Time:")[1].strip()
        
        # Parse content statistics
        elif "Content Statistics" in line:
            current_section = "content_stats"
        elif current_section == "content_stats" and "│" in line:
            parts = [p.strip() for p in line.split("│") if p.strip()]
            if len(parts) >= 3:
                metric = parts[0]
                count = parts[1]
                details = parts[2]
                structured["content_statistics"][metric] = {"count": count, "details": details}
        
        # Parse test results
        elif "Functionality Test Results" in line:
            current_section = "test_results"
        elif current_section == "test_results" and "│" in line:
            parts = [p.strip() for p in line.split("│") if p.strip()]
            if len(parts) >= 4:
                test_name = parts[0]
                status = parts[1]
                details = parts[2]
                time = parts[3]
                structured["test_results"].append({
                    "test": test_name,
                    "status": status,
                    "details": details,
                    "time": time
                })
        
        # Parse AI analysis
        elif "AI-Powered Content Analysis" in line:
            current_section = "ai_analysis"
        elif current_section == "ai_analysis":
            if "Final Assessment" in line:
                current_section = "final_assessment"
            else:
                ai_analysis_lines.append(line)
        
        # Parse final assessment
        elif "Final Assessment" in line:
            current_section = "final_assessment"
        elif current_section == "final_assessment" and "│" in line:
            if "Overall Assessment:" in line:
                structured["final_assessment"]["overall"] = line.split("Overall Assessment:")[1].strip()
            elif "Success Rate:" in line:
                structured["final_assessment"]["success_rate"] = line.split("Success Rate:")[1].strip()
            elif "Recommendation:" in line:
                structured["final_assessment"]["recommendation"] = line.split("Recommendation:")[1].strip()
    
    structured["ai_analysis"] = "\n".join(ai_analysis_lines)
    
    return structured

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast_to_session(self, message: str, session_id: str):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(json.dumps({
                        "type": "output",
                        "message": message,
                        "timestamp": asyncio.get_event_loop().time()
                    }))
                except:
                    # Remove dead connections
                    self.active_connections[session_id].remove(connection)

manager = ConnectionManager()

async def broadcast_output(session_id: str, message: str):
    """Broadcast output to all connected WebSocket clients for this session"""
    await manager.broadcast_to_session(message, session_id)

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 