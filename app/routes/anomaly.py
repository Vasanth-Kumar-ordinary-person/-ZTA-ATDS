from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
import torch
import json
import asyncio
from app.models.autoencoder import LogAutoEncoder
from app.utils.connection_manager import manager
from app.utils.alerting import process_anomaly_alert
from app.utils.realtime_streamer import streamer, get_streamer_stats
from app.utils.prediction import predict_anomaly

router = APIRouter()

INPUT_DIM = 5  # Update based on your dataset
model = LogAutoEncoder(INPUT_DIM)
model.load_state_dict(torch.load("model.pt"))
model.eval()

class LogData(BaseModel):
    features: list[float]

@router.post("/predict-anomaly/")
async def predict_anomaly_endpoint(data: LogData):
    """Predict anomaly for given data"""
    result = await predict_anomaly(data.features)
    return result

@router.post("/stream-predict/")
async def stream_predict(data: LogData):
    """Real-time streaming prediction endpoint"""
    result = await predict_anomaly(data.features)
    
    # Always broadcast real-time predictions
    stream_data = {
        "type": "prediction",
        "data": result
    }
    await manager.broadcast(json.dumps(stream_data))
    
    return result

@router.post("/start-monitoring/")
async def start_monitoring():
    """Start real-time monitoring"""
    try:
        if not streamer.is_running:
            asyncio.create_task(streamer.start_streaming())
            await manager.broadcast(json.dumps({
                "type": "monitoring_status",
                "status": "started",
                "message": "Real-time monitoring started"
            }))
            return {"status": "success", "message": "Monitoring started"}
        else:
            return {"status": "already_running", "message": "Monitoring already running"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/stop-monitoring/")
async def stop_monitoring():
    """Stop real-time monitoring"""
    try:
        if streamer.is_running:
            await streamer.stop_streaming()
            await manager.broadcast(json.dumps({
                "type": "monitoring_status",
                "status": "stopped",
                "message": "Real-time monitoring stopped"
            }))
            return {"status": "success", "message": "Monitoring stopped"}
        else:
            return {"status": "not_running", "message": "Monitoring not running"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/monitoring-status/")
async def get_monitoring_status():
    """Get current monitoring status"""
    stats = get_streamer_stats()
    return {
        "is_running": stats["is_running"],
        "processed_count": stats["processed_count"],
        "anomaly_count": stats["anomaly_count"],
        "uptime": stats["uptime"]
    }

@router.post("/test-anomaly/")
async def test_anomaly():
    """Test anomaly detection with high values"""
    test_features = [10.0, 10.0, 10.0, 10.0, 10.0]  # High values to trigger anomaly
    result = await predict_anomaly(test_features)
    
    # Broadcast test result
    await manager.broadcast(json.dumps({
        "type": "test_anomaly",
        "data": result,
        "message": f"Test anomaly detected: Score={result['anomaly_score']:.4f}"
    }))
    
    return result

@router.get("/health")
async def health_check():
    """Health check endpoint for real-time monitoring"""
    return {
        "status": "healthy",
        "model_loaded": True,
        "active_connections": len(manager.active_connections)
    }