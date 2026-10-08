import asyncio
import math
import random
import time
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(
    title="STD Track Telemetry Engine",
    description="Real-time multi-modal transport streaming server (Airplanes, Trains, Ships, Buses, Cars)",
    version="1.0.0"
)

# CORS configuration for Vercel and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initial Telemetry Dataset
INITIAL_FLEET: List[Dict[str, Any]] = [
    # ✈️ Airplanes
    {
        "id": "AI-161",
        "callsign": "AIC161",
        "category": "flight",
        "operator": "Air India Express",
        "origin": {"code": "DEL", "city": "New Delhi", "lat": 28.5562, "lon": 77.1000},
        "dest": {"code": "LHR", "city": "London Heathrow", "lat": 51.4700, "lon": -0.4543},
        "lat": 29.8,
        "lon": 74.2,
        "speed": 840,
        "altitude": 36000,
        "heading": 295,
        "status": "Cruising - On Time",
        "eta": "21:30 UTC",
        "fuel": 88,
        "squawk": "4712",
        "transponder": "Mode-S ADS-B",
        "source": "OpenSky Network Stream"
    },
    {
        "id": "6E-204",
        "callsign": "IGO204",
        "category": "flight",
        "operator": "IndiGo Airlines",
        "origin": {"code": "BOM", "city": "Mumbai", "lat": 19.0896, "lon": 72.8656},
        "dest": {"code": "DEL", "city": "New Delhi", "lat": 28.5562, "lon": 77.1000},
        "lat": 23.4,
        "lon": 74.9,
        "speed": 780,
        "altitude": 32000,
        "heading": 32,
        "status": "En Route",
        "eta": "15:45 UTC",
        "fuel": 76,
        "squawk": "1254",
        "transponder": "Mode-S ADS-B",
        "source": "ADS-B Exchange"
    },
    {
        "id": "EK-501",
        "callsign": "UAE501",
        "category": "flight",
        "operator": "Emirates A380",
        "origin": {"code": "DXB", "city": "Dubai", "lat": 25.2532, "lon": 55.3657},
        "dest": {"code": "BOM", "city": "Mumbai", "lat": 19.0896, "lon": 72.8656},
        "lat": 21.8,
        "lon": 67.5,
        "speed": 910,
        "altitude": 39000,
        "heading": 115,
        "status": "Descending",
        "eta": "16:10 UTC",
        "fuel": 64,
        "squawk": "3310",
        "transponder": "Mode-S ADS-B",
        "source": "OpenSky Network"
    },
    # 🚆 Trains
    {
        "id": "VB-22436",
        "callsign": "VANDE-BHARAT",
        "category": "train",
        "operator": "Indian Railways (NR)",
        "origin": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "dest": {"code": "BSB", "city": "Varanasi Jn", "lat": 25.3283, "lon": 82.9739},
        "lat": 26.8467,
        "lon": 80.9462,
        "speed": 130,
        "altitude": 125,
        "heading": 110,
        "status": "Approaching Kanpur Yard",
        "eta": "14:15 UTC",
        "fuel": 98,
        "squawk": "VB-01",
        "transponder": "GPS / RTIS ISRO Satellite",
        "source": "CRIS / GTFS-Realtime"
    },
    {
        "id": "RAJ-12952",
        "callsign": "RAJDHANI-EXP",
        "category": "train",
        "operator": "Western Railway",
        "origin": {"code": "MMCT", "city": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        "dest": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "lat": 22.3072,
        "lon": 73.1812,
        "speed": 120,
        "altitude": 90,
        "heading": 18,
        "status": "Running On Time",
        "eta": "08:35 UTC",
        "fuel": 95,
        "squawk": "WR-12952",
        "transponder": "RTIS Telemetry",
        "source": "IRCTC / GTFS-RT"
    },
    # 🚢 Ships
    {
        "id": "EVER-GIVEN",
        "callsign": "H3RC",
        "category": "ship",
        "operator": "Evergreen Marine Corp",
        "origin": {"code": "PKG", "city": "Port Klang", "lat": 2.9999, "lon": 101.3928},
        "dest": {"code": "ROT", "city": "Rotterdam", "lat": 51.9244, "lon": 4.4777},
        "lat": 12.8,
        "lon": 53.2,
        "speed": 38,
        "altitude": 0,
        "heading": 260,
        "status": "Transit Gulf of Aden",
        "eta": "4d 12h",
        "fuel": 80,
        "squawk": "MMSI 353136000",
        "transponder": "Class A AIS",
        "source": "AISHub / MarineTraffic"
    },
    {
        "id": "INS-VIKRANT",
        "callsign": "R11",
        "category": "ship",
        "operator": "Indian Navy (Carrier)",
        "origin": {"code": "COK", "city": "Kochi Fleet Base", "lat": 9.9312, "lon": 76.2673},
        "dest": {"code": "GOA", "city": "Goa Naval Ops", "lat": 15.3857, "lon": 73.8370},
        "lat": 13.5,
        "lon": 74.1,
        "speed": 46,
        "altitude": 0,
        "heading": 340,
        "status": "Active Fleet Patrol",
        "eta": "Routine",
        "fuel": 91,
        "squawk": "SECURE-TAC",
        "transponder": "Military AIS / TACAN",
        "source": "Naval Maritime Ops"
    },
    # 🚌 Buses
    {
        "id": "DL-VOLVO-99",
        "callsign": "HR-68B-1090",
        "category": "bus",
        "operator": "Haryana Roadways Volvo",
        "origin": {"code": "ISBT", "city": "Delhi Kashmiri Gate", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "CDG", "city": "Chandigarh Sec 17", "lat": 30.7333, "lon": 76.7794},
        "lat": 29.5,
        "lon": 76.9,
        "speed": 85,
        "altitude": 235,
        "heading": 345,
        "status": "GT Road Express Corridor",
        "eta": "18:00 UTC",
        "fuel": 72,
        "squawk": "HR-GPS-99",
        "transponder": "AIS-140 GPS Tracker",
        "source": "State Transit GTFS-RT"
    },
    # 🚗 Cars
    {
        "id": "CAB-DEL-VIP1",
        "callsign": "EV-NEXON-01",
        "category": "car",
        "operator": "BluSmart EV Fleet Delhi",
        "origin": {"code": "IGI-T3", "city": "Indira Gandhi Airport", "lat": 28.5562, "lon": 77.1000},
        "dest": {"code": "CP", "city": "Connaught Place", "lat": 28.6315, "lon": 77.2167},
        "lat": 28.59,
        "lon": 77.16,
        "speed": 55,
        "altitude": 215,
        "heading": 52,
        "status": "Trip in Progress",
        "eta": "14 mins",
        "fuel": 84,
        "squawk": "EV-FLEET-DEL",
        "transponder": "OBD-II Telematics",
        "source": "BluSmart Fleet Telemetry"
    }
]

# In-memory fleet state
vehicles: List[Dict[str, Any]] = [dict(v) for v in INITIAL_FLEET]

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(data)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

# Background dead-reckoning simulation task
async def dead_reckoning_loop():
    while True:
        try:
            for v in vehicles:
                speed_factor = (v["speed"] / 3600.0) * 0.012
                rad = math.radians(v["heading"])
                v["lat"] += math.cos(rad) * speed_factor
                v["lon"] += math.sin(rad) * speed_factor

                # Micro fluctuations
                if random.random() > 0.7:
                    v["heading"] = (v["heading"] + random.randint(-2, 2) + 360) % 360
                if random.random() > 0.8:
                    v["speed"] = max(15, v["speed"] + random.randint(-3, 3))

            # Broadcast to all connected WebSockets
            if manager.active_connections:
                payload = {
                    "type": "telemetry_update",
                    "timestamp": time.time(),
                    "vehicles": vehicles
                }
                await manager.broadcast(payload)

        except Exception as e:
            print("Error in simulation loop:", e)

        await asyncio.sleep(1.0)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dead_reckoning_loop())

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "STD Track Telemetry Engine",
        "active_vehicles": len(vehicles),
        "connected_clients": len(manager.active_connections),
        "supported_modes": ["flight", "train", "ship", "bus", "car"]
    }

@app.get("/api/vehicles")
def get_vehicles():
    return {"vehicles": vehicles}

@app.get("/api/opensky/live")
async def get_opensky_live():
    """Proxy fetch to OpenSky Network ADS-B API to avoid client-side CORS issues"""
    try:
        url = "https://opensky-network.org/api/states/all?lamin=8&lomin=68&lamax=35&lomax=97"
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                return {"success": True, "states": data.get("states", [])[:30]}
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": False, "error": "Failed to fetch from OpenSky"}

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await manager.connect(websocket)
    # Send initial snapshot immediately upon connection
    await websocket.send_json({
        "type": "initial_state",
        "timestamp": time.time(),
        "vehicles": vehicles
    })
    try:
        while True:
            # Receive client ping or filter preferences
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
