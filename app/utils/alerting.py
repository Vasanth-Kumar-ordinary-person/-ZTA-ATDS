import asyncio
import json
import time
from typing import Dict, Any, List
from app.utils.connection_manager import manager

class AlertManager:
    """Real-time alerting system for anomaly detection"""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules = {
            "high_anomaly_score": 0.1,
            "consecutive_anomalies": 3,
            "anomaly_rate_threshold": 0.5
        }
        self.recent_anomalies = []
        self.is_running = False
    
    async def start_alerting(self):
        """Start the alerting system"""
        self.is_running = True
        asyncio.create_task(self._monitor_alerts())
    
    async def stop_alerting(self):
        """Stop the alerting system"""
        self.is_running = False
    
    async def process_anomaly(self, anomaly_data: Dict[str, Any]):
        """Process a new anomaly detection"""
        timestamp = time.time()
        
        # Add to recent anomalies list
        self.recent_anomalies.append({
            "timestamp": timestamp,
            "score": anomaly_data.get("anomaly_score", 0),
            "data": anomaly_data
        })
        
        # Keep only last 100 anomalies
        if len(self.recent_anomalies) > 100:
            self.recent_anomalies = self.recent_anomalies[-100:]
        
        # Check alert conditions
        await self._check_alert_conditions(anomaly_data)
    
    async def _check_alert_conditions(self, anomaly_data: Dict[str, Any]):
        """Check if alert conditions are met"""
        score = anomaly_data.get("anomaly_score", 0)
        
        # High anomaly score alert
        if score > self.alert_rules["high_anomaly_score"]:
            await self._send_alert("HIGH_ANOMALY_SCORE", {
                "score": score,
                "threshold": self.alert_rules["high_anomaly_score"],
                "message": f"High anomaly score detected: {score:.4f}"
            })
        
        # Consecutive anomalies alert
        recent_count = len([a for a in self.recent_anomalies[-10:] if a["score"] > 0.05])
        if recent_count >= self.alert_rules["consecutive_anomalies"]:
            await self._send_alert("CONSECUTIVE_ANOMALIES", {
                "count": recent_count,
                "threshold": self.alert_rules["consecutive_anomalies"],
                "message": f"Multiple consecutive anomalies detected: {recent_count}"
            })
        
        # Anomaly rate alert
        if len(self.recent_anomalies) >= 20:
            recent_anomalies = [a for a in self.recent_anomalies[-20:] if a["score"] > 0.05]
            anomaly_rate = len(recent_anomalies) / 20
            if anomaly_rate > self.alert_rules["anomaly_rate_threshold"]:
                await self._send_alert("HIGH_ANOMALY_RATE", {
                    "rate": anomaly_rate,
                    "threshold": self.alert_rules["anomaly_rate_threshold"],
                    "message": f"High anomaly rate detected: {anomaly_rate:.2%}"
                })
    
    async def _send_alert(self, alert_type: str, alert_data: Dict[str, Any]):
        """Send an alert to connected clients"""
        alert = {
            "type": "alert",
            "alert_type": alert_type,
            "timestamp": time.time(),
            "severity": self._get_severity(alert_type),
            "data": alert_data
        }
        
        self.alerts.append(alert)
        
        # Keep only last 50 alerts
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]
        
        # Broadcast alert
        await manager.broadcast(json.dumps(alert))
        
        # Log alert
        print(f"ALERT: {alert_type} - {alert_data.get('message', '')}")
    
    def _get_severity(self, alert_type: str) -> str:
        """Get severity level for alert type"""
        severity_map = {
            "HIGH_ANOMALY_SCORE": "HIGH",
            "CONSECUTIVE_ANOMALIES": "MEDIUM",
            "HIGH_ANOMALY_RATE": "HIGH"
        }
        return severity_map.get(alert_type, "LOW")
    
    async def _monitor_alerts(self):
        """Background task for alert monitoring"""
        while self.is_running:
            # Send periodic alert summary
            if self.alerts:
                summary = {
                    "type": "alert_summary",
                    "timestamp": time.time(),
                    "total_alerts": len(self.alerts),
                    "recent_alerts": self.alerts[-5:],  # Last 5 alerts
                    "anomaly_stats": {
                        "total_recent": len(self.recent_anomalies),
                        "high_score_count": len([a for a in self.recent_anomalies if a["score"] > 0.1])
                    }
                }
                await manager.broadcast(json.dumps(summary))
            
            await asyncio.sleep(30)  # Send summary every 30 seconds
    
    def get_alert_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get alert history"""
        return self.alerts[-limit:] if self.alerts else []
    
    def get_anomaly_stats(self) -> Dict[str, Any]:
        """Get anomaly statistics"""
        if not self.recent_anomalies:
            return {"total": 0, "high_score": 0, "rate": 0}
        
        total = len(self.recent_anomalies)
        high_score = len([a for a in self.recent_anomalies if a["score"] > 0.1])
        rate = len([a for a in self.recent_anomalies if a["score"] > 0.05]) / total
        
        return {
            "total": total,
            "high_score": high_score,
            "rate": rate
        }

# Global alert manager instance
alert_manager = AlertManager()

async def start_alerting():
    """Start the alerting system"""
    await alert_manager.start_alerting()

async def stop_alerting():
    """Stop the alerting system"""
    await alert_manager.stop_alerting()

async def process_anomaly_alert(anomaly_data: Dict[str, Any]):
    """Process an anomaly for alerting"""
    await alert_manager.process_anomaly(anomaly_data)

def get_alert_stats():
    """Get alerting statistics"""
    return {
        "is_running": alert_manager.is_running,
        "total_alerts": len(alert_manager.alerts),
        "anomaly_stats": alert_manager.get_anomaly_stats()
    } 