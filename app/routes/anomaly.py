from fastapi import APIRouter
from pydantic import BaseModel
import torch
from app.models.autoencoder import LogAutoEncoder

router = APIRouter()

INPUT_DIM = 5  # Update based on your dataset
model = LogAutoEncoder(INPUT_DIM)
model.load_state_dict(torch.load("model.pt"))
model.eval()

class LogData(BaseModel):
    features: list[float]

@router.post("/predict-anomaly/")
def predict_anomaly(data: LogData):
    x = torch.tensor([data.features], dtype=torch.float32)
    with torch.no_grad():
        recon = model(x)
        score = torch.nn.functional.mse_loss(x, recon).item()
        return {"anomaly_score": score, "is_anomalous": score > 0.05}