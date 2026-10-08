# 📡 STD Track — Realtime Telemetry Backend (FastAPI, Scrapers & WebSockets)

Real-time multi-modal telemetry streaming engine for **STD Track**. Scrapes and streams live updates for:
- ✈️ **Airplanes:** Live commercial flights scraped from **FlightRadar24 ADS-B** & **OpenSky Network**.
- 🚢 **Ships:** Real-time maritime vessels from **Digitraffic Open AIS** & strategic sea lanes (Ever Given, Maersk).
- 🚆 **Trains:** High-precision track progression across **Indian Railways corridors** (Vande Bharat, Rajdhani, Gatimaan).
- 🚌 **Buses & 🚗 Cars:** Live state transport (Volvo, KSRTC) & urban EV fleet telematics.

---

## ⚡ Architecture & Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `WS` | `/ws/telemetry` | High-frequency 1Hz JSON stream for live map rendering. |
| `GET` | `/` | Health check & active scraped source statistics. |
| `GET` | `/api/vehicles` | Instant JSON snapshot of all active vehicles across categories. |
| `GET` | `/api/scraped/flights` | Raw scraped commercial flights from FlightRadar24 / OpenSky. |
| `GET` | `/api/scraped/ships` | Raw AIS merchant vessel positions. |
| `POST` | `/api/refresh` | Force an immediate re-scrape of external APIs. |

---

## 🚀 Local Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with uvicorn
uvicorn main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000`
- WebSocket stream: `ws://localhost:8000/ws/telemetry`

---

## ☁️ Deployment

### Deploy on Heroku:
1. Connect your GitHub repository `LuciferRJ29/std-track-backend` in the Heroku Dashboard.
2. Heroku automatically detects `Procfile` (`web: uvicorn main:app --host 0.0.0.0 --port $PORT`) and `requirements.txt`.
3. Click **Deploy Branch**.

### Deploy on Render / Railway:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
