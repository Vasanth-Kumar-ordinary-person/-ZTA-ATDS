import torch
import asyncio
from app.models.autoencoder import LogAutoEncoder
from app.utils.connection_manager import manager
from app.utils.alerting import process_anomaly_alert
import json

# Load model
INPUT_DIM = 5  # Update based on your dataset
model = LogAutoEncoder(INPUT_DIM)
model.load_state_dict(torch.load("model.pt"))
model.eval()

async def predict_anomaly(features):
    """Predict anomaly for given features"""
    x = torch.tensor([features], dtype=torch.float32)
    with torch.no_grad():
        recon = model(x)
        score = torch.nn.functional.mse_loss(x, recon).item()
        is_anomalous = score > 0.05
        
        result = {
            "anomaly_score": score, 
            "is_anomalous": is_anomalous,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Broadcast anomaly detection to all connected WebSocket clients
        if is_anomalous:
            alert_data = {
                "type": "anomaly_alert",
                "data": result,
                "message": f"Anomaly detected! Score: {score:.4f}"
            }
            await manager.broadcast(json.dumps(alert_data))
            
            # Process for alerting system
            await process_anomaly_alert(result)
        
        return result 