import asyncio
import json
import logging
import math
import random
import time
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from scrapers.flight_scraper import scrape_flights
from scrapers.ship_scraper import scrape_ships
from scrapers.rail_engine import calculate_train_positions
from scrapers.transit_engine import calculate_transit_positions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("std_track")

app = FastAPI(
    title="STD Track Telemetry Engine",
    description="Worldwide Realtime Multi-Modal Telemetry Engine (FlightRadar24 + OpenSky + AIS Ships + Indian Railways + Global Transit)",
    version="2.5.2"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Master in-memory fleet state
live_flights: List[Dict[str, Any]] = []
live_ships: List[Dict[str, Any]] = []
all_vehicles: List[Dict[str, Any]] = []

def to_compact(v: Dict[str, Any]) -> Dict[str, Any]:
    orig = v.get("origin", {})
    dest = v.get("dest", {})
    return {
        "id": v["id"],
        "cat": v.get("category", "flight"),
        "op": (v.get("operator") or "Commercial Transport")[:25],
        "ac": (v.get("aircraft") or "")[:18],
        "lat": round(float(v["lat"]), 3),
        "lon": round(float(v["lon"]), 3),
        "spd": int(v.get("speed", 0)),
        "alt": int(v.get("altitude", 0)),
        "hdg": int(v.get("heading", 0)),
        "o": (orig.get("code", "DEP") if isinstance(orig, dict) else "DEP")[:8],
        "oc": (orig.get("city", "Departure") if isinstance(orig, dict) else str(orig))[:20],
        "d": (dest.get("code", "ARR") if isinstance(dest, dict) else "ARR")[:8],
        "dc": (dest.get("city", "Destination") if isinstance(dest, dict) else str(dest))[:20],
        "st": (v.get("status", "Active") or "Active")[:22],
        "sq": str(v.get("squawk", "4701"))[:8],
        "src": (v.get("source", "Live Telemetry") or "Live Telemetry")[:18]
    }

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Active clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Active clients: {len(self.active_connections)}")

    async def broadcast(self, data: dict):
        if not self.active_connections:
            return
        # High-performance zero-whitespace single-pass serialization (keeps frame size compact)
        msg = json.dumps(data, separators=(',', ':'))
        for connection in list(self.active_connections):
            try:
                await connection.send_text(msg)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

# Background Task 1: Periodic Scraper Loop (FlightRadar24 ADS-B + AIS Ships)
async def periodic_scraper_loop():
    global live_flights, live_ships
    while True:
        try:
            logger.info("Executing global multi-zone scrape for flights and ships...")
            scraped_f = await scrape_flights(limit=1800)
            if scraped_f:
                live_flights = scraped_f
                logger.info(f"Updated live flights: {len(live_flights)}")

            scraped_s = await scrape_ships(limit=250)
            if scraped_s:
                live_ships = scraped_s
                logger.info(f"Updated live ships: {len(live_ships)}")

        except Exception as e:
            logger.error(f"Error in scraper loop: {e}")

        # Refresh scrape every 20 seconds
        await asyncio.sleep(20.0)

# Background Task 2: Real-time Telemetry Broadcast & Dead-Reckoning Loop
async def high_frequency_telemetry_loop():
    global all_vehicles
    while True:
        try:
            # 1. Update dead-reckoning on live flights
            for f in live_flights:
                speed_factor = (f.get("speed", 500) / 3600.0) * 0.02
                rad = math.radians(f.get("heading", 0))
                f["lat"] += math.cos(rad) * speed_factor
                f["lon"] += math.sin(rad) * speed_factor
                if random.random() > 0.85:
                    f["heading"] = (f["heading"] + random.randint(-1, 1) + 360) % 360

            # 2. Update dead-reckoning on live ships
            for s in live_ships:
                speed_factor = (s.get("speed", 25) / 3600.0) * 0.015
                rad = math.radians(s.get("heading", 0))
                s["lat"] += math.cos(rad) * speed_factor
                s["lon"] += math.sin(rad) * speed_factor

            # 3. Compute real-time trains & transit
            trains = calculate_train_positions()
            transit = calculate_transit_positions()

            # 4. Merge all active transport categories
            all_vehicles = live_flights + live_ships + trains + transit

            # 5. Broadcast compact payload to connected WebSocket clients (keeps frame well under 500KB)
            if manager.active_connections:
                payload = {
                    "type": "telemetry_update",
                    "timestamp": time.time(),
                    "stats": {
                        "flights": len(live_flights),
                        "ships": len(live_ships),
                        "trains": len(trains),
                        "transit": len(transit),
                        "total": len(all_vehicles)
                    },
                    "vehicles": [to_compact(v) for v in all_vehicles]
                }
                await manager.broadcast(payload)

        except Exception as e:
            logger.error(f"Error in telemetry broadcast loop: {e}")

        await asyncio.sleep(2.0)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting STD Track Worldwide Telemetry Engine...")
    async def initial_harvest():
        global live_flights, live_ships, all_vehicles
        try:
            live_flights = await scrape_flights(limit=1800)
            live_ships = await scrape_ships(limit=250)
            trains = calculate_train_positions()
            transit = calculate_transit_positions()
            all_vehicles = live_flights + live_ships + trains + transit
            logger.info(f"Initial harvest complete! Total active fleet: {len(all_vehicles)}")
        except Exception as e:
            logger.warning(f"Initial harvest error: {e}")

    asyncio.create_task(initial_harvest())
    asyncio.create_task(periodic_scraper_loop())
    asyncio.create_task(high_frequency_telemetry_loop())

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "STD Track Scraper & Telemetry Engine",
        "version": "2.5.1",
        "scraped_sources": {
            "flights": "FlightRadar24 ADS-B (8 Global Zones) & OpenSky Network",
            "ships": "Digitraffic Open AIS & Global Sea Lanes",
            "trains": "Indian Railways (CRIS/RTIS) Corridors & World High Speed Rail",
            "transit": "State Roadways (Volvo, KSRTC) & Intercity Transit"
        },
        "stats": {
            "active_vehicles": len(all_vehicles),
            "live_flights": len(live_flights),
            "live_ships": len(live_ships),
            "live_trains": len([v for v in all_vehicles if v.get("category") == "train"]),
            "live_transit": len([v for v in all_vehicles if v.get("category") in ["bus", "car"]]),
            "connected_clients": len(manager.active_connections)
        }
    }

@app.get("/api/vehicles")
def get_vehicles():
    """Returns instant snapshot of all currently active vehicles across categories."""
    return {
        "count": len(all_vehicles),
        "vehicles": [to_compact(v) for v in all_vehicles]
    }

@app.get("/api/scraped/flights")
async def get_scraped_flights():
    """Returns currently scraped live flights from FlightRadar24 / OpenSky."""
    return {"count": len(live_flights), "flights": live_flights}

@app.get("/api/scraped/ships")
async def get_scraped_ships():
    """Returns currently scraped live vessels from AIS."""
    return {"count": len(live_ships), "ships": live_ships}

@app.post("/api/refresh")
async def force_refresh():
    """Triggers an immediate re-scrape of external APIs."""
    global live_flights, live_ships
    live_flights = await scrape_flights(limit=2000)
    live_ships = await scrape_ships(limit=250)
    return {
        "status": "refreshed",
        "flights_count": len(live_flights),
        "ships_count": len(live_ships)
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await manager.connect(websocket)
    # Send immediate state on handshake with compact format (<450KB frame)
    await websocket.send_json({
        "type": "initial_state",
        "timestamp": time.time(),
        "stats": {
            "flights": len(live_flights),
            "ships": len(live_ships),
            "total": len(all_vehicles)
        },
        "vehicles": [to_compact(v) for v in all_vehicles]
    })
    try:
        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
