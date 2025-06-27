# ZTA-ATDS: Zero Trust AI-Powered Threat Detection System

ZTA-ATDS is a lightweight, AI-based anomaly detection system designed to detect abnormal system behavior using unsupervised machine learning. It uses an autoencoder neural network trained on normal system logs to flag deviations, integrating seamlessly with cybersecurity workflows.

---

## 🚀 Features

- FastAPI-based REST API for real-time threat prediction
- PyTorch autoencoder trained on system-level metrics (CPU, Memory, Disk, etc.)
- Threshold-based anomaly scoring
- Logs inference results for Splunk/SIEM integration
- Modular and extensible architecture

---

## 🧠 Tech Stack

- Python 3.9+
- PyTorch
- FastAPI
- pandas, scikit-learn
- Uvicorn (ASGI server)
- Optional: Splunk for log analysis

---




---

## 🔧 Installation

```bash
git clone https://github.com/<your-username>/zta-atds.git
cd zta-atds
python -m venv venv
venv\Scripts\activate        # On Windows
pip install -r requirements.txt
🧪 Training the Model
bash
Copy code
python -m train.train_model
This trains the autoencoder using data/logs.csv and saves the model as model.pt.

🌐 Running the API
bash
Copy code
uvicorn app.main:app --reload
Visit http://127.0.0.1:8000/docs for Swagger UI.

📬 Sample Request
Endpoint:
bash
Copy code
POST /predict-anomaly/
JSON Input:
json
Copy code
{
  "features": [10, 40, 20, 5, 30]
}
Response:
json
Copy code
{
  "anomaly_score": 0.0042,
  "is_anomalous": false
}
📈 Splunk Integration (Optional)
All inference requests are logged in inference.log. You can configure Splunk to monitor this file:

plaintext
Copy code
index=main source="inference.log" sourcetype=log
📌 Next Improvements
SHAP-based model explainability

Streamlit-based real-time dashboard

Ingest Windows Event Logs (via Sysmon or Winlogbeat)

Auto-retraining pipeline with live logs

Docker containerization for deployment

🤝 Contributing
Want to improve or extend this? Fork the repo, make changes, and submit a PR. All contributions are welcome!

📄 License
MIT License

📬 Contact
For feedback, questions, or collaborations, feel free to reach out via LinkedIn or GitHub.

markdown
Copy code

---

## 🔤 Repository Name Suggestions

Here are some name ideas depending on tone and audience:

### 🔒 **Security-Focused**
- `zero-trust-anomaly-detector`
- `zta-inference-engine`
- `ai-threat-detector`
- `ml-soc-anomaly-detection`

### 🧠 **AI-Focused**
- `autoencoder-threat-detector`
- `torch-anomaly-detection-api`
- `unsupervised-anomaly-pipeline`

### 🧪 **General or Open Source-Style**
- `zta-atds`
- `anomaly-lens`
- `log-guardian`
- `threatwatch-ai`

Let me know your preferred tone and I can help you fina
