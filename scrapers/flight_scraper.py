import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

AIRLINE_NAMES = {
    "AIC": "Air India",
    "IGO": "IndiGo",
    "SEJ": "SpiceJet",
    "VTI": "Vistara",
    "AXB": "Air India Express",
    "AKJ": "Akasa Air",
    "UAE": "Emirates",
    "ETD": "Etihad Airways",
    "QTR": "Qatar Airways",
    "BAW": "British Airways",
    "DLH": "Lufthansa",
    "SIA": "Singapore Airlines"
}

async def scrape_flights(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Scrapes real live commercial flights from FlightRadar24 ADS-B feed across
    Eurasia, Middle East, India, and Southeast Asian corridors.
    """
    flights: List[Dict[str, Any]] = []

    # Source 1: FlightRadar24 Wide Transcontinental Airspace Stream
    try:
        # Wide bounding box: Europe, Middle East, India, SE Asia (Lat: 0-55, Lon: 20-120)
        fr24_url = "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=55,0,20,120"
        async with httpx.AsyncClient(timeout=8.0, headers=HEADERS) as client:
            res = await client.get(fr24_url)
            if res.status_code == 200:
                data = res.json()
                keys = [k for k in data.keys() if k not in ["full_count", "version", "stats"]]
                for key in keys[:limit]:
                    item = data[key]
                    if not isinstance(item, list) or len(item) < 14:
                        continue

                    callsign = item[16] or item[13] or f"FLT-{key[:6]}"
                    flight_num = item[13] or callsign
                    airline_code = item[18] or (callsign[:3] if len(callsign) >= 3 else "")
                    operator = AIRLINE_NAMES.get(airline_code, f"{airline_code} Airline" if airline_code else "Commercial Flight")
                    origin_code = item[11] or "DEP"
                    dest_code = item[12] or "ARR"
                    lat = float(item[1])
                    lon = float(item[2])
                    heading = int(item[3]) if item[3] else 0
                    alt_ft = int(item[4]) if item[4] else 0
                    speed_kts = int(item[5]) if item[5] else 250
                    speed_kmh = int(speed_kts * 1.852)

                    flights.append({
                        "id": flight_num,
                        "callsign": callsign,
                        "category": "flight",
                        "operator": operator,
                        "aircraft": item[8] or "Commercial Jet",
                        "origin": {"code": origin_code, "city": origin_code, "lat": lat - 1.5, "lon": lon - 1.5},
                        "dest": {"code": dest_code, "city": dest_code, "lat": lat + 1.5, "lon": lon + 1.5},
                        "lat": lat,
                        "lon": lon,
                        "speed": speed_kmh,
                        "altitude": alt_ft,
                        "heading": heading,
                        "status": "Airborne (Live ADS-B)",
                        "eta": "In Flight",
                        "fuel": 82,
                        "squawk": str(item[6] or "4701"),
                        "transponder": "Mode-S ADS-B",
                        "source": "FlightRadar24 Scraper"
                    })

                if flights:
                    logger.info(f"Successfully scraped {len(flights)} flights from FlightRadar24")
                    return flights
    except Exception as e:
        logger.warning(f"FlightRadar24 scrape failed: {e}. Trying OpenSky fallback...")

    # Source 2: OpenSky Network Fallback
    try:
        opensky_url = "https://opensky-network.org/api/states/all?lamin=8&lomin=68&lamax=35&lomax=96"
        async with httpx.AsyncClient(timeout=8.0, headers=HEADERS) as client:
            res = await client.get(opensky_url)
            if res.status_code == 200:
                data = res.json()
                states = data.get("states", [])
                for s in states[:limit]:
                    callsign = (s[1] or "FLT").strip() or f"OS-{s[0]}"
                    lat = float(s[6]) if s[6] is not None else 20.0
                    lon = float(s[5]) if s[5] is not None else 78.0
                    speed_kmh = int((s[9] or 200) * 3.6)
                    alt_ft = int((s[7] or 9000) * 3.28084)
                    heading = int(s[10] or 0)

                    flights.append({
                        "id": callsign,
                        "callsign": callsign,
                        "category": "flight",
                        "operator": s[2] or "Commercial Airline",
                        "aircraft": "ICAO Aircraft",
                        "origin": {"code": "DEP", "city": "Departure", "lat": lat - 1.0, "lon": lon - 1.0},
                        "dest": {"code": "ARR", "city": "Arrival", "lat": lat + 1.0, "lon": lon + 1.0},
                        "lat": lat,
                        "lon": lon,
                        "speed": speed_kmh,
                        "altitude": alt_ft,
                        "heading": heading,
                        "status": "Airborne (OpenSky)",
                        "eta": "In Transit",
                        "fuel": 80,
                        "squawk": str(s[14] or "7000"),
                        "transponder": "OpenSky Network Feed",
                        "source": "OpenSky Scraper"
                    })
    except Exception as e:
        logger.error(f"OpenSky fallback failed: {e}")

    return flights
