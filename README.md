# ZTA-ATDS - Zero Trust AI Threat Detection System

## Real-Time Threat Detection System

ZTA-ATDS is now a **real-time** threat detection system with live monitoring, WebSocket communication, and instant alerting capabilities.

## 🚀 Real-Time Features

### ✨ New Real-Time Capabilities
- **Live WebSocket Dashboard** - Real-time monitoring interface
- **Instant Anomaly Detection** - Continuous threat monitoring
- **Real-Time Alerting** - Immediate notifications for threats
- **Live Data Streaming** - Continuous log processing
- **Performance Monitoring** - Real-time system metrics

### 🔧 Technical Components
- **FastAPI Backend** with WebSocket support
- **Autoencoder AI Model** for anomaly detection
- **Real-time Data Processing** pipeline
- **Live Alerting System** with configurable rules
- **Interactive Dashboard** with live updates

## 🛠️ Installation & Setup

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the Real-Time Application:**
```bash
python run_realtime.py
```

3. **Access the Dashboard:**
   - Open your browser to: `http://localhost:8000`
   - Real-time dashboard will load automatically
   - WebSocket connection established automatically

## 📊 Real-Time Dashboard Features

### Live Monitoring
- **Connection Status** - Real-time WebSocket connectivity
- **System Health** - Model status and active connections
- **Performance Metrics** - Throughput and response times
- **Live Log Stream** - Real-time data processing logs

### Interactive Controls
- **Start/Stop Monitoring** - Control real-time data processing
- **Test Anomaly** - Trigger test anomaly detection
- **Live Alerts** - Real-time threat notifications

### Real-Time Metrics
- **Processed Logs** - Count of analyzed data points
- **Anomalies Detected** - Number of threats identified
- **System Uptime** - Continuous monitoring duration
- **Throughput** - Logs processed per second

## 🔌 API Endpoints

### Real-Time Endpoints
- `GET /` - Real-time dashboard
- `WS /ws` - WebSocket connection for live updates
- `POST /predict-anomaly/` - Single anomaly detection
- `POST /stream-predict/` - Real-time streaming prediction
- `GET /health` - System health check

### WebSocket Events
- `anomaly_alert` - Threat detection notifications
- `prediction` - Real-time prediction results
- `system_monitoring` - Live system metrics
- `alert` - Alert system notifications
- `alert_summary` - Periodic alert summaries

## 🚨 Alert System

### Alert Types
- **HIGH_ANOMALY_SCORE** - High threat score detected
- **CONSECUTIVE_ANOMALIES** - Multiple threats in sequence
- **HIGH_ANOMALY_RATE** - Elevated threat frequency

### Alert Configuration
```python
alert_rules = {
    "high_anomaly_score": 0.1,      # Score threshold
    "consecutive_anomalies": 3,      # Consecutive count
    "anomaly_rate_threshold": 0.5    # Rate percentage
}
```

## 🔄 Real-Time Data Flow

1. **Data Ingestion** - Continuous log data streaming
2. **AI Processing** - Real-time anomaly detection
3. **Alert Generation** - Instant threat notifications
4. **Dashboard Updates** - Live metric updates
5. **WebSocket Broadcasting** - Real-time client updates

## 📈 Performance Features

- **Low Latency** - Sub-second response times
- **High Throughput** - Continuous data processing
- **Scalable Architecture** - Async processing
- **Fault Tolerance** - Automatic reconnection
- **Real-time Metrics** - Live performance monitoring

## 🎯 Usage Examples

### Start Real-Time Monitoring
```bash
# Start the application
python run_realtime.py

# Access dashboard
open http://localhost:8000
```

### Test Real-Time Features
1. Open the dashboard
2. Click "Start Monitoring" for continuous processing
3. Click "Test Anomaly" to trigger test detection
4. Watch real-time alerts and metrics

### API Testing
```bash
# Test anomaly detection
curl -X POST "http://localhost:8000/predict-anomaly/" \
     -H "Content-Type: application/json" \
     -d '{"features": [1.0, 2.0, 3.0, 4.0, 5.0]}'

# Test streaming prediction
curl -X POST "http://localhost:8000/stream-predict/" \
     -H "Content-Type: application/json" \
     -d '{"features": [1.0, 2.0, 3.0, 4.0, 5.0]}'
```

## 🔧 Configuration

### Environment Variables
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `LOG_LEVEL` - Logging level (default: info)

### Model Configuration
- Update `INPUT_DIM` in `app/routes/anomaly.py` for your dataset
- Adjust anomaly threshold in the same file
- Modify alert rules in `app/utils/alerting.py`

## 🚀 Production Deployment

For production deployment, consider:
- **Load Balancing** - Multiple server instances
- **Database Integration** - Persistent storage
- **Message Queue** - Redis/RabbitMQ for scaling
- **Monitoring** - Prometheus/Grafana integration
- **Security** - HTTPS/WSS for production

## 📝 License

This project is licensed under the MIT License.