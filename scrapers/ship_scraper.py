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
    # 🇮🇳 India - JNPT / Navi Mumbai Container Ship
    {
        "id": "MAERSK-MUMBAI",
        "callsign": "OWGQ2",
        "category": "ship",
        "operator": "A.P. Moller - Maersk (India)",
        "origin": {"code": "JEA", "city": "Dubai Jebel Ali", "lat": 24.9857, "lon": 55.0273},
        "dest": {"code": "JNPT", "city": "Navi Mumbai JNPT Port", "lat": 18.9499, "lon": 72.9515},
        "lat": 18.82,
        "lon": 72.45,
        "speed": 34,
        "altitude": 0,
        "heading": 85,
        "status": "Approaching JNPT Outer Channel",
        "eta": "04:30 UTC",
        "fuel": 85,
        "squawk": "MMSI 219018501",
        "transponder": "Class A AIS",
        "source": "JNPT Port Telematics"
    },
    # 🇮🇳 India - Indian Navy Aircraft Carrier (Arabian Sea Patrol)
    {
        "id": "INS-VIKRANT",
        "callsign": "R11",
        "category": "ship",
        "operator": "Indian Navy (Carrier Strike Group)",
        "origin": {"code": "COK", "city": "Kochi Fleet Base", "lat": 9.9312, "lon": 76.2673},
        "dest": {"code": "GOA", "city": "Goa Naval Ops", "lat": 15.3857, "lon": 73.8370},
        "lat": 14.2,
        "lon": 73.2,
        "speed": 46,
        "altitude": 0,
        "heading": 340,
        "status": "Active Western Fleet Patrol",
        "eta": "Mission Active",
        "fuel": 92,
        "squawk": "SECURE-TAC",
        "transponder": "Military AIS / TACAN",
        "source": "Naval Maritime Operations"
    },
    # 🇮🇳 India - Crude Oil Tanker in Gulf of Kutch / Kandla
    {
        "id": "IOCL-KANDLA-TANKER",
        "callsign": "DESH-SHANTI",
        "category": "ship",
        "operator": "Shipping Corp of India (SCI)",
        "origin": {"code": "BASRA", "city": "Basra Oil Terminal (Iraq)", "lat": 29.6800, "lon": 48.8000},
        "dest": {"code": "KANDLA", "city": "Deendayal Port Kandla (India)", "lat": 23.0033, "lon": 70.2186},
        "lat": 22.75,
        "lon": 69.10,
        "speed": 28,
        "altitude": 0,
        "heading": 65,
        "status": "Gulf of Kutch Crude Corridor",
        "eta": "12:00 UTC",
        "fuel": 88,
        "squawk": "MMSI 419000120",
        "transponder": "Class A AIS",
        "source": "SCI Fleet Telematics"
    },
    # 🇮🇳 India - Chennai Port Container Carrier (Bay of Bengal)
    {
        "id": "MSC-CHENNAI-EXPRESS",
        "callsign": "MSC-CH99",
        "category": "ship",
        "operator": "Mediterranean Shipping Co (MSC)",
        "origin": {"code": "SIN", "city": "Singapore Port", "lat": 1.2902, "lon": 103.8519},
        "dest": {"code": "MAA-PORT", "city": "Chennai Port Container Terminal", "lat": 13.0839, "lon": 80.2989},
        "lat": 12.90,
        "lon": 81.20,
        "speed": 36,
        "altitude": 0,
        "heading": 290,
        "status": "Bay of Bengal Sea Lane",
        "eta": "16:45 UTC",
        "fuel": 79,
        "squawk": "MMSI 355912000",
        "transponder": "Class A AIS",
        "source": "Chennai Port Trust AIS"
    },
    # 🇮🇳 India - Cochin Port LNG Carrier
    {
        "id": "GAIL-COCHIN-LNG",
        "callsign": "LNG-BHARAT-01",
        "category": "ship",
        "operator": "Petronet LNG / GAIL",
        "origin": {"code": "RAS-LAFFAN", "city": "Ras Laffan (Qatar)", "lat": 25.9000, "lon": 51.5300},
        "dest": {"code": "COK-LNG", "city": "Kochi LNG Terminal Puthuvype", "lat": 9.9900, "lon": 76.2200},
        "lat": 10.15,
        "lon": 75.80,
        "speed": 32,
        "altitude": 0,
        "heading": 135,
        "status": "Approaching Kochi Channel",
        "eta": "08:15 UTC",
        "fuel": 90,
        "squawk": "MMSI 419000888",
        "transponder": "Class A AIS",
        "source": "Petronet Telematics"
    },
    # 🌍 Suez Canal - Ever Given
    {
        "id": "EVER-GIVEN",
        "callsign": "H3RC",
        "category": "ship",
        "operator": "Evergreen Marine Corp",
        "origin": {"code": "PKG", "city": "Port Klang (Malaysia)", "lat": 2.9999, "lon": 101.3928},
        "dest": {"code": "ROT", "city": "Rotterdam (Netherlands)", "lat": 51.9244, "lon": 4.4777},
        "lat": 29.8,
        "lon": 32.55,
        "speed": 22,
        "altitude": 0,
        "heading": 340,
        "status": "Transit Suez Canal Northbound",
        "eta": "3d 10h",
        "fuel": 80,
        "squawk": "MMSI 353136000",
        "transponder": "Class A AIS",
        "source": "Suez Canal Authority Feed"
    },
    # 🌍 Strait of Malacca - Supertanker
    {
        "id": "FRONT-ALTAIR",
        "callsign": "LAEY7",
        "category": "ship",
        "operator": "Frontline Ltd (VLCC)",
        "origin": {"code": "FUJ", "city": "Fujairah (UAE)", "lat": 25.1288, "lon": 56.3265},
        "dest": {"code": "YOK", "city": "Yokohama (Japan)", "lat": 35.4437, "lon": 139.6380},
        "lat": 2.5,
        "lon": 101.8,
        "speed": 30,
        "altitude": 0,
        "heading": 125,
        "status": "Strait of Malacca Deepwater Lane",
        "eta": "6d 04h",
        "fuel": 84,
        "squawk": "MMSI 538008172",
        "transponder": "Class A AIS",
        "source": "Malacca Strait AIS"
    }
]

async def scrape_ships(limit: int = 35) -> List[Dict[str, Any]]:
    """
    Scrapes live merchant vessels from open AIS streams and merges
    with dedicated Indian port vessels and international trade lanes.
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
                    sog = props.get("sog", 10.0)
                    cog = props.get("cog", 0.0)
                    heading = int(props.get("heading", cog) if props.get("heading", 511) != 511 else cog)
                    lon = float(coords[0])
                    lat = float(coords[1])

                    if sog < 1.0:
                        continue

                    ships.append({
                        "id": f"VESSEL-{mmsi}",
                        "callsign": f"MMSI-{mmsi}",
                        "category": "ship",
                        "operator": f"Merchant Cargo Ship ({mmsi})",
                        "origin": {"code": "PORT-A", "city": "European Port", "lat": lat - 0.5, "lon": lon - 0.5},
                        "dest": {"code": "PORT-B", "city": "Open Sea", "lat": lat + 0.5, "lon": lon + 0.5},
                        "lat": lat,
                        "lon": lon,
                        "speed": int(sog * 1.852),
                        "altitude": 0,
                        "heading": heading,
                        "status": "Underway Using Engine",
                        "eta": "En Route",
                        "fuel": 88,
                        "squawk": f"MMSI {mmsi}",
                        "transponder": "Class A AIS",
                        "source": "Digitraffic Live AIS Feed"
                    })

                logger.info(f"Loaded {len(ships)} vessels.")
    except Exception as e:
        logger.warning(f"AIS scrape error: {e}")

    return ships
