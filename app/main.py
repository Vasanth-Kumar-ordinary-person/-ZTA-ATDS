from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import anomaly
from app.utils.connection_manager import manager
import asyncio
import json
from typing import List

app = FastAPI(title="ZTA-ATDS API")

app.include_router(anomaly.router)

# Serve static files for the dashboard
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_dashboard():
    with open("static/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for testing
            await manager.send_personal_message(f"Message received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task for real-time monitoring
@app.on_event("startup")
async def startup_event():
    # Start background monitoring task
    asyncio.create_task(background_monitoring())
    
    # Start alerting system only (streaming will be controlled by user)
    from app.utils.alerting import start_alerting
    
    asyncio.create_task(start_alerting())

async def background_monitoring():
    """Background task for continuous monitoring"""
    while True:
        # Simulate real-time data processing
        await asyncio.sleep(5)  # Check every 5 seconds
        # In a real implementation, this would process actual log data
        monitoring_data = {
            "timestamp": asyncio.get_event_loop().time(),
            "status": "monitoring",
            "processed_logs": 0,
            "anomalies_detected": 0
        }
        await manager.broadcast(json.dumps(monitoring_data))