import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Encoding": "gzip"
}

# Major international & Indian maritime routes
FLAG_SHIPS = [
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
        "id": "MAERSK-MC",
        "callsign": "OWGQ2",
        "category": "ship",
        "operator": "A.P. Moller - Maersk",
        "origin": {"code": "JEA", "city": "Jebel Ali", "lat": 24.9857, "lon": 55.0273},
        "dest": {"code": "JNPT", "city": "Navi Mumbai", "lat": 18.9499, "lon": 72.9515},
        "lat": 19.3,
        "lon": 69.8,
        "speed": 34,
        "altitude": 0,
        "heading": 95,
        "status": "Approaching Coastal Waters",
        "eta": "07:15 UTC",
        "fuel": 85,
        "squawk": "MMSI 219018501",
        "transponder": "Class A AIS",
        "source": "Global Maritime Feed"
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
    }
]

async def scrape_ships(limit: int = 30) -> List[Dict[str, Any]]:
    """
    Scrapes live merchant vessels from open AIS streams (Digitraffic AIS)
    and merges with strategic maritime corridor vessels.
    """
    ships: List[Dict[str, Any]] = [dict(s) for s in FLAG_SHIPS]

    try:
        url = "https://meri.digitraffic.fi/api/ais/v1/locations"
        async with httpx.AsyncClient(timeout=8.0, headers=HEADERS) as client:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                features = data.get("features", [])
                for f in features[:limit]:
                    coords = f.get("geometry", {}).get("coordinates", [])
                    props = f.get("properties", {})
                    if len(coords) < 2:
                        continue

                    mmsi = props.get("mmsi")
                    sog = props.get("sog", 10.0) # Speed over ground in knots
                    cog = props.get("cog", 0.0)  # Course over ground in degrees
                    heading = int(props.get("heading", cog) if props.get("heading", 511) != 511 else cog)
                    lon = float(coords[0])
                    lat = float(coords[1])

                    # Filter out static anchored ships with speed < 1 knot
                    if sog < 1.0:
                        continue

                    ships.append({
                        "id": f"VESSEL-{mmsi}",
                        "callsign": f"MMSI-{mmsi}",
                        "category": "ship",
                        "operator": f"Cargo / Merchant Vessel ({mmsi})",
                        "origin": {"code": "PORT-A", "city": "Open Sea", "lat": lat - 0.5, "lon": lon - 0.5},
                        "dest": {"code": "PORT-B", "city": "Sea Corridor", "lat": lat + 0.5, "lon": lon + 0.5},
                        "lat": lat,
                        "lon": lon,
                        "speed": int(sog * 1.852), # convert knots to km/h for uniform telemetry
                        "altitude": 0,
                        "heading": heading,
                        "status": "Underway Using Engine",
                        "eta": "En Route",
                        "fuel": 88,
                        "squawk": f"MMSI {mmsi}",
                        "transponder": "Class A AIS",
                        "source": "Digitraffic Live AIS Feed"
                    })

                logger.info(f"Loaded {len(ships)} ships from AIS feed.")
    except Exception as e:
        logger.warning(f"AIS scrape failed: {e}. Using flag ships.")

    return ships
