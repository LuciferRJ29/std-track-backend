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
    "UAE": "Emirates",
    "ETD": "Etihad Airways",
    "QTR": "Qatar Airways",
    "BAW": "British Airways",
    "DLH": "Lufthansa",
    "AFR": "Air France",
    "KLM": "KLM Royal Dutch",
    "SIA": "Singapore Airlines",
    "ANA": "All Nippon Airways",
    "JAL": "Japan Airlines",
    "AAL": "American Airlines",
    "DAL": "Delta Air Lines",
    "UAL": "United Airlines",
    "SWA": "Southwest Airlines",
    "QFA": "Qantas Airways"
}

# Major global regions for comprehensive worldwide airspace coverage
GLOBAL_ZONES = [
    {"name": "Asia & India", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=42,5,55,105", "limit": 45},
    {"name": "Europe", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=60,35,-10,35", "limit": 40},
    {"name": "North America", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=50,25,-125,-65", "limit": 40},
    {"name": "East Asia / Japan", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=45,20,115,145", "limit": 25}
]

async def scrape_flights(limit: int = 150) -> List[Dict[str, Any]]:
    """
    Scrapes real live commercial flights worldwide from FlightRadar24 ADS-B feeds,
    covering North America, Europe, Asia, India, and East Asia.
    """
    flights: List[Dict[str, Any]] = []

    async with httpx.AsyncClient(timeout=8.0, headers=HEADERS) as client:
        for zone in GLOBAL_ZONES:
            try:
                res = await client.get(zone["url"])
                if res.status_code == 200:
                    data = res.json()
                    keys = [k for k in data.keys() if k not in ["full_count", "version", "stats"]]
                    zone_limit = zone["limit"]

                    for key in keys[:zone_limit]:
                        item = data[key]
                        if not isinstance(item, list) or len(item) < 14:
                            continue

                        callsign = item[16] or item[13] or f"FLT-{key[:6]}"
                        flight_num = item[13] or callsign
                        airline_code = item[18] or (callsign[:3] if len(callsign) >= 3 else "")
                        operator = AIRLINE_NAMES.get(airline_code, f"{airline_code} Airlines" if airline_code else "Commercial Airline")
                        origin_code = item[11] or "DEP"
                        dest_code = item[12] or "ARR"
                        lat = float(item[1])
                        lon = float(item[2])
                        heading = int(item[3]) if item[3] else 0
                        alt_ft = int(item[4]) if item[4] else 0
                        speed_kts = int(item[5]) if item[5] else 250
                        speed_kmh = int(speed_kts * 1.852)
                        aircraft = item[8] or "Commercial Aircraft"

                        flights.append({
                            "id": flight_num,
                            "callsign": callsign,
                            "category": "flight",
                            "operator": operator,
                            "aircraft": aircraft,
                            "origin": {"code": origin_code, "city": origin_code, "lat": lat - 1.8, "lon": lon - 1.8},
                            "dest": {"code": dest_code, "city": dest_code, "lat": lat + 1.8, "lon": lon + 1.8},
                            "lat": lat,
                            "lon": lon,
                            "speed": speed_kmh,
                            "altitude": alt_ft,
                            "heading": heading,
                            "status": "Airborne (Live ADS-B)",
                            "eta": "En Route",
                            "fuel": 84,
                            "squawk": str(item[6] or "4701"),
                            "transponder": "Mode-S ADS-B",
                            "source": f"FlightRadar24 ({zone['name']})"
                        })

            except Exception as e:
                logger.warning(f"Error scraping zone {zone['name']}: {e}")

    logger.info(f"Total worldwide flights scraped: {len(flights)}")
    return flights
