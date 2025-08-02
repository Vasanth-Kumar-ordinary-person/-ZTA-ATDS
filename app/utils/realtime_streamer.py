import asyncio
import json
import time
import random
from typing import AsyncGenerator, Dict, Any
from app.utils.connection_manager import manager
from app.utils.prediction import predict_anomaly

class RealTimeStreamer:
    """Real-time data streaming and processing utility"""
    
    def __init__(self):
        self.is_running = False
        self.processed_count = 0
        self.anomaly_count = 0
        self.start_time = None
        
    async def start_streaming(self):
        """Start real-time data streaming"""
        self.is_running = True
        self.start_time = time.time()
        
        # Start background monitoring task
        asyncio.create_task(self._background_monitoring())
        
        # Start data streaming
        async for data in self._generate_log_data():
            if not self.is_running:
                break
                
            await self._process_log_data(data)
    
    async def stop_streaming(self):
        """Stop real-time data streaming"""
        self.is_running = False
    
    async def _generate_log_data(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate simulated log data in real-time"""
        while self.is_running:
            # Simulate log data generation
            log_entry = {
                "timestamp": time.time(),
                "source": "system_logs",
                "level": random.choice(["INFO", "WARNING", "ERROR"]),
                "message": f"Log entry {self.processed_count}",
                "features": [
                    random.uniform(0, 5),  # Feature 1
                    random.uniform(0, 5),  # Feature 2
                    random.uniform(0, 5),  # Feature 3
                    random.uniform(0, 5),  # Feature 4
                    random.uniform(0, 5)   # Feature 5
                ]
            }
            
            yield log_entry
            await asyncio.sleep(1)  # Generate data every second
    
    async def _process_log_data(self, log_data: Dict[str, Any]):
        """Process log data through anomaly detection"""
        try:
            # Extract features for anomaly detection
            features = log_data["features"]
            
            # Get prediction using the separate prediction module
            result = await predict_anomaly(features)
            
            # Update counters
            self.processed_count += 1
            if result["is_anomalous"]:
                self.anomaly_count += 1
            
            # Broadcast real-time update
            await self._broadcast_update(log_data, result)
            
        except Exception as e:
            print(f"Error processing log data: {e}")
    
    async def _broadcast_update(self, log_data: Dict[str, Any], prediction_result: Dict[str, Any]):
        """Broadcast real-time updates to connected clients"""
        update_data = {
            "type": "log_processed",
            "timestamp": time.time(),
            "log_data": log_data,
            "prediction": prediction_result,
            "stats": {
                "processed_count": self.processed_count,
                "anomaly_count": self.anomaly_count,
                "uptime": time.time() - self.start_time if self.start_time else 0
            }
        }
        
        await manager.broadcast(json.dumps(update_data))
    
    async def _background_monitoring(self):
        """Background task for system monitoring"""
        while self.is_running:
            monitoring_data = {
                "type": "system_monitoring",
                "timestamp": time.time(),
                "status": "active",
                "processed_logs": self.processed_count,
                "anomalies_detected": self.anomaly_count,
                "uptime": time.time() - self.start_time if self.start_time else 0,
                "throughput": self.processed_count / max(1, (time.time() - self.start_time)) if self.start_time else 0
            }
            
            await manager.broadcast(json.dumps(monitoring_data))
            await asyncio.sleep(5)  # Update every 5 seconds

# Global streamer instance
streamer = RealTimeStreamer()

async def start_realtime_streaming():
    """Start the real-time streaming service"""
    await streamer.start_streaming()

async def stop_realtime_streaming():
    """Stop the real-time streaming service"""
    await streamer.stop_streaming()

def get_streamer_stats():
    """Get current streaming statistics"""
    return {
        "is_running": streamer.is_running,
        "processed_count": streamer.processed_count,
        "anomaly_count": streamer.anomaly_count,
        "uptime": time.time() - streamer.start_time if streamer.start_time else 0
    } 