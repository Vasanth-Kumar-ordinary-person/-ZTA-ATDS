from fastapi import FastAPI
from app.routes import anomaly

app = FastAPI(title="ZTA-ATDS API")
app.include_router(anomaly.router)