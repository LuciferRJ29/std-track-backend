import asyncio
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
    description="Real-time multi-modal transport streaming server (FlightRadar24 + OpenSky + AIS Ships + Indian Railways)",
    version="2.0.0"
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

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Remaining clients: {len(self.active_connections)}")

    async def broadcast(self, data: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(data)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

# Background Task 1: Periodic Scraper Loop (FlightRadar24 + AIS Ships)
async def periodic_scraper_loop():
    global live_flights, live_ships
    while True:
        try:
            logger.info("Executing periodic live scrape for flights and ships...")
            scraped_f = await scrape_flights(limit=160)
            if scraped_f:
                live_flights = scraped_f
                logger.info(f"Updated live flights: {len(live_flights)}")

            scraped_s = await scrape_ships(limit=35)
            if scraped_s:
                live_ships = scraped_s
                logger.info(f"Updated live ships: {len(live_ships)}")

        except Exception as e:
            logger.error(f"Error in scraper loop: {e}")

        # Wait 15 seconds before next live scrape cycle to respect external API limits
        await asyncio.sleep(15.0)

# Background Task 2: High-frequency 1Hz WebSocket Broadcast & Dead-Reckoning
async def high_frequency_telemetry_loop():
    global all_vehicles
    while True:
        try:
            # 1. Update dead-reckoning on live flights
            for f in live_flights:
                speed_factor = (f["speed"] / 3600.0) * 0.012
                rad = math.radians(f["heading"])
                f["lat"] += math.cos(rad) * speed_factor
                f["lon"] += math.sin(rad) * speed_factor
                if random.random() > 0.8:
                    f["heading"] = (f["heading"] + random.randint(-1, 1) + 360) % 360

            # 2. Update dead-reckoning on live ships
            for s in live_ships:
                speed_factor = (s["speed"] / 3600.0) * 0.008
                rad = math.radians(s["heading"])
                s["lat"] += math.cos(rad) * speed_factor
                s["lon"] += math.sin(rad) * speed_factor

            # 3. Compute real-time trains & transit
            trains = calculate_train_positions()
            transit = calculate_transit_positions()

            # 4. Merge all active transport categories
            all_vehicles = live_flights + live_ships + trains + transit

            # 5. Broadcast to connected WebSocket clients
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
                    "vehicles": all_vehicles
                }
                await manager.broadcast(payload)

        except Exception as e:
            logger.error(f"Error in telemetry broadcast loop: {e}")

        await asyncio.sleep(1.0)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting STD Track Telemetry Engine...")
    # Initial immediate scrape
    asyncio.create_task(periodic_scraper_loop())
    asyncio.create_task(high_frequency_telemetry_loop())

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "STD Track Scraper & Telemetry Engine",
        "version": "2.0.0",
        "scraped_sources": {
            "flights": "FlightRadar24 ADS-B & OpenSky Network",
            "ships": "Digitraffic Open AIS & Global Sea Lanes",
            "trains": "Indian Railways (CRIS/RTIS) Corridors & SNCF",
            "transit": "State Roadways (Volvo, KSRTC) & City EV Fleets"
        },
        "stats": {
            "active_vehicles": len(all_vehicles),
            "live_flights": len(live_flights),
            "live_ships": len(live_ships),
            "connected_clients": len(manager.active_connections)
        }
    }

@app.get("/api/vehicles")
def get_vehicles():
    """Returns instant snapshot of all currently active vehicles across categories."""
    return {
        "count": len(all_vehicles),
        "vehicles": all_vehicles
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
    live_flights = await scrape_flights(limit=40)
    live_ships = await scrape_ships(limit=25)
    return {
        "status": "refreshed",
        "flights_count": len(live_flights),
        "ships_count": len(live_ships)
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await manager.connect(websocket)
    # Send immediate state on handshake
    await websocket.send_json({
        "type": "initial_state",
        "timestamp": time.time(),
        "vehicles": all_vehicles
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
