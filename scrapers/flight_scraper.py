import asyncio
import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

AIRLINE_NAMES = {
    # 🇮🇳 India & South Asia
    "IGO": "IndiGo Airlines",
    "AIC": "Air India",
    "AXB": "Air India Express",
    "SEJ": "SpiceJet",
    "VTI": "Vistara",
    "AKJ": "Akasa Air",
    "BPA": "Blue Dart Aviation",
    "SDG": "Star Air",
    "PIA": "Pakistan Int'l Airlines",
    "BBC": "Biman Bangladesh",
    "ALK": "SriLankan Airlines",
    # 🌍 Middle East & Gulf
    "UAE": "Emirates",
    "ETD": "Etihad Airways",
    "QTR": "Qatar Airways",
    "FDB": "Flydubai",
    "GFA": "Gulf Air",
    "OMA": "Oman Air",
    "SVA": "Saudia",
    "RJA": "Royal Jordanian",
    # 🇪🇺 Europe
    "BAW": "British Airways",
    "DLH": "Lufthansa",
    "AFR": "Air France",
    "KLM": "KLM Royal Dutch",
    "IBE": "Iberia",
    "AZA": "ITA Airways",
    "SWR": "Swiss Int'l Air Lines",
    "AUA": "Austrian Airlines",
    "SAS": "Scandinavian Airlines",
    "FIN": "Finnair",
    "TAP": "TAP Air Portugal",
    "LOT": "LOT Polish Airlines",
    "RYR": "Ryanair",
    "EZY": "easyJet",
    "WZZ": "Wizz Air",
    "THY": "Turkish Airlines",
    # 🇺🇸 North America
    "AAL": "American Airlines",
    "DAL": "Delta Air Lines",
    "UAL": "United Airlines",
    "SWA": "Southwest Airlines",
    "JBU": "JetBlue Airways",
    "ASA": "Alaska Airlines",
    "FFT": "Frontier Airlines",
    "ACA": "Air Canada",
    "WJA": "WestJet",
    "AMX": "Aeromexico",
    # 🇯🇵 Asia & Oceania
    "SIA": "Singapore Airlines",
    "ANA": "All Nippon Airways",
    "JAL": "Japan Airlines",
    "CPA": "Cathay Pacific",
    "THA": "Thai Airways",
    "MAS": "Malaysia Airlines",
    "GIA": "Garuda Indonesia",
    "KAL": "Korean Air",
    "AAR": "Asiana Airlines",
    "EVA": "EVA Air",
    "CAL": "China Airlines",
    "CCA": "Air China",
    "CES": "China Eastern",
    "CSN": "China Southern",
    "QFA": "Qantas Airways",
    "VOZ": "Virgin Australia",
    "ANZ": "Air New Zealand",
    # 🌎 South America & Africa
    "LAN": "LATAM Airlines",
    "GLO": "Gol Transportes Aéreos",
    "AZU": "Azul Brazilian Airlines",
    "AVA": "Avianca",
    "ETH": "Ethiopian Airlines",
    "EGY": "EgyptAir",
    "RAM": "Royal Air Maroc",
    "SAA": "South African Airways",
    "KQA": "Kenya Airways"
}

# 8 Worldwide Quadrants covering all continents and oceans
ZONES = [
    # 🇮🇳 Zone 1: Indian Subcontinent (Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Goa)
    {"name": "India Airspace", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=36,8,68,97", "limit": 200},
    # 🇪🇺 Zone 2: Europe (London, Paris, Frankfurt, Amsterdam, Madrid, Rome)
    {"name": "Europe Airspace", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=65,30,-15,40", "limit": 350},
    # 🇺🇸 Zone 3: North America (New York, LA, Chicago, Atlanta, Dallas, Toronto)
    {"name": "North America", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=60,15,-130,-60", "limit": 450},
    # 🇨🇳 Zone 4: East Asia & Pacific Rim (Tokyo, Beijing, Shanghai, Seoul, Singapore, Bangkok)
    {"name": "East Asia & Pacific", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=45,1,100,145", "limit": 350},
    # 🌍 Zone 5: Middle East & Gulf (Dubai, Doha, Abu Dhabi, Riyadh, Istanbul)
    {"name": "Middle East & Gulf", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=35,15,45,65", "limit": 150},
    # 🌎 Zone 6: South America (São Paulo, Buenos Aires, Bogota, Lima, Santiago)
    {"name": "South America", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=15,-55,-85,-35", "limit": 150},
    # 🇦🇺 Zone 7: Oceania & Australia (Sydney, Melbourne, Brisbane, Auckland, Perth)
    {"name": "Oceania & Australia", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=-10,-48,110,180", "limit": 150},
    # 🌍 Zone 8: Africa (Cairo, Johannesburg, Nairobi, Lagos, Casablanca)
    {"name": "Africa Airspace", "url": "https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds=38,-35,-20,55", "limit": 150}
]

# Keep a robust cache so if any zone temporarily fails or throttles, the sky stays full
cached_flights: List[Dict[str, Any]] = []

async def fetch_zone(client: httpx.AsyncClient, zone: Dict[str, Any]) -> List[Dict[str, Any]]:
    zone_flights: List[Dict[str, Any]] = []
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
                operator = AIRLINE_NAMES.get(airline_code, f"{airline_code} Airlines" if airline_code and len(airline_code) == 3 else "Commercial Air Transport")
                origin_code = item[11] or "DEP"
                dest_code = item[12] or "ARR"
                lat = float(item[1])
                lon = float(item[2])
                heading = int(item[3]) if item[3] else 0
                alt_ft = int(item[4]) if item[4] else 32000
                speed_kts = int(item[5]) if item[5] else 450
                speed_kmh = int(speed_kts * 1.852)
                aircraft = item[8] or "Boeing / Airbus Jet"

                zone_flights.append({
                    "id": flight_num,
                    "callsign": callsign,
                    "category": "flight",
                    "operator": operator,
                    "aircraft": aircraft,
                    "origin": {"code": origin_code, "city": origin_code, "lat": lat - 1.5, "lon": lon - 1.5},
                    "dest": {"code": dest_code, "city": dest_code, "lat": lat + 1.5, "lon": lon + 1.5},
                    "lat": lat,
                    "lon": lon,
                    "speed": speed_kmh,
                    "altitude": alt_ft,
                    "heading": heading,
                    "status": "Airborne (Live ADS-B)",
                    "eta": "En Route",
                    "fuel": 82,
                    "squawk": str(item[6] or "4701"),
                    "transponder": "Mode-S ADS-B",
                    "source": f"FlightRadar24 ({zone['name']})"
                })
    except Exception as e:
        logger.warning(f"Error scraping zone {zone['name']}: {e}")
    return zone_flights

async def scrape_flights(limit: int = 2000) -> List[Dict[str, Any]]:
    """
    Scrapes real live commercial flights from FlightRadar24 ADS-B across all 8 global zones.
    If throttled, falls back to OpenSky Network global feed.
    """
    global cached_flights
    flights: List[Dict[str, Any]] = []

    async with httpx.AsyncClient(timeout=8.0, headers=HEADERS) as client:
        tasks = [fetch_zone(client, zone) for zone in ZONES]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for res in results:
            if isinstance(res, list):
                flights.extend(res)

    # If FR24 returned a rich set, update cache
    if len(flights) >= 200:
        cached_flights = flights[:limit]
        logger.info(f"Total live commercial flights scraped across all continents: {len(cached_flights)}")
        return cached_flights

    # Fallback to OpenSky Network if FR24 returned too few
    try:
        logger.info("Attempting OpenSky fallback harvest...")
        async with httpx.AsyncClient(timeout=9.0, headers=HEADERS) as client:
            os_res = await client.get("https://opensky-network.org/api/states/all")
            if os_res.status_code == 200:
                os_data = os_res.json()
                states = os_data.get("states", [])
                for s in states[:800]:
                    if not s[5] or not s[6]:
                        continue
                    icao = s[0]
                    callsign = (s[1] or f"OS-{icao}").strip()
                    lon = float(s[5])
                    lat = float(s[6])
                    alt_m = s[7] or 10000
                    alt_ft = int(alt_m * 3.28084)
                    vel_ms = s[9] or 220
                    speed_kmh = int(vel_ms * 3.6)
                    heading = int(s[10]) if s[10] is not None else 0

                    airline_code = callsign[:3] if len(callsign) >= 3 else ""
                    operator = AIRLINE_NAMES.get(airline_code, f"{s[2]} Transport" if s[2] else "Civil Aircraft")

                    flights.append({
                        "id": callsign,
                        "callsign": callsign,
                        "category": "flight",
                        "operator": operator,
                        "aircraft": "Commercial Jet",
                        "origin": {"code": "DEP", "city": "Departure", "lat": lat - 1.2, "lon": lon - 1.2},
                        "dest": {"code": "ARR", "city": "Destination", "lat": lat + 1.2, "lon": lon + 1.2},
                        "lat": lat,
                        "lon": lon,
                        "speed": speed_kmh,
                        "altitude": alt_ft,
                        "heading": heading,
                        "status": "Airborne (OpenSky)",
                        "eta": "En Route",
                        "fuel": 80,
                        "squawk": str(s[14] or "1200"),
                        "transponder": "OpenSky Network Mode-S",
                        "source": "OpenSky ADS-B"
                    })
    except Exception as e:
        logger.warning(f"OpenSky fallback error: {e}")

    if flights:
        cached_flights = flights[:limit]
        return cached_flights
    return cached_flights
