# 📡 STD Track — Realtime Telemetry Backend (FastAPI & WebSockets)

Real-time multi-modal telemetry streaming engine for **STD Track**. Streams dynamic updates for Airplanes ✈️, Trains 🚆, Ships 🚢, Buses 🚌, and Cars 🚗.

---

## ⚡ Features
- **WebSocket Gateway:** `/ws/telemetry` pushes updates every 1 second to all connected dashboards.
- **Dead-Reckoning Engine:** Simulates realistic movement along headings and speeds.
- **OpenSky ADS-B Proxy:** `/api/opensky/live` retrieves real commercial flights.
- **Heroku / Render / Railway Ready:** Pre-configured with `Procfile`, `runtime.txt`, and CORS headers.

---

## 🚀 Local Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with uvicorn
uvicorn main:app --reload --port 8000
```
Open in browser: `http://localhost:8000` (Health check)  
WebSocket stream: `ws://localhost:8000/ws/telemetry`

---

## ☁️ Deployment

### Deploy on Heroku:
1. Connect your GitHub repository `LuciferRJ29/std-track-backend` in the Heroku Dashboard.
2. Enable Automatic Deploys from `main`.
3. Heroku will automatically detect `Procfile` and `requirements.txt`.

### Deploy on Render / Railway:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
