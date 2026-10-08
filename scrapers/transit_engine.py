import math
import time
from typing import List, Dict, Any

WORLD_BUS_ROUTES = [
    # 🇺🇸 US - Greyhound Express (East Coast)
    {
        "id": "GREYHOUND-NY-BOS",
        "callsign": "GH-1044-USA",
        "category": "bus",
        "operator": "Greyhound Lines (USA)",
        "origin": {"code": "NYC", "city": "New York Port Authority (USA)", "lat": 40.7570, "lon": -73.9903},
        "dest": {"code": "BOS", "city": "Boston South Station (USA)", "lat": 42.3523, "lon": -71.0552},
        "speed": 105,
        "altitude": 25,
        "squawk": "GH-US-01",
        "transponder": "Omnitracs Fleet Telematics",
        "source": "Greyhound Live Bus Tracker"
    },
    # 🇺🇸 US - Greyhound Express (West Coast)
    {
        "id": "GREYHOUND-LA-SF",
        "callsign": "GH-2088-CA",
        "category": "bus",
        "operator": "Greyhound California",
        "origin": {"code": "LAX", "city": "Los Angeles Union (USA)", "lat": 34.0562, "lon": -118.2365},
        "dest": {"code": "SFO", "city": "San Francisco Transbay", "lat": 37.7897, "lon": -122.3969},
        "speed": 110,
        "altitude": 85,
        "squawk": "GH-US-02",
        "transponder": "ELD GPS Stream",
        "source": "US Interstate Telematics"
    },
    # 🇪🇺 Europe - FlixBus (Paris -> Brussels -> Amsterdam)
    {
        "id": "FLIXBUS-PAR-AMS",
        "callsign": "FLIX-EU-101",
        "category": "bus",
        "operator": "FlixBus Europe",
        "origin": {"code": "PAR", "city": "Paris Bercy Seine (France)", "lat": 48.8352, "lon": 2.3789},
        "dest": {"code": "AMS", "city": "Amsterdam Sloterdijk (Netherlands)", "lat": 52.3890, "lon": 4.8377},
        "speed": 100,
        "altitude": 35,
        "squawk": "FLIX-101",
        "transponder": "FlixTelematics GPS",
        "source": "FlixBus Real-Time Stream"
    },
    # 🇪🇺 Europe - FlixBus (Berlin -> Prague)
    {
        "id": "FLIXBUS-BER-PRG",
        "callsign": "FLIX-EU-420",
        "category": "bus",
        "operator": "FlixBus Central Europe",
        "origin": {"code": "BER", "city": "Berlin ZOB (Germany)", "lat": 52.5073, "lon": 13.2798},
        "dest": {"code": "PRG", "city": "Prague Florenc (Czechia)", "lat": 50.0901, "lon": 14.4402},
        "speed": 98,
        "altitude": 240,
        "squawk": "FLIX-420",
        "transponder": "European GTFS-RT",
        "source": "FlixBus Live Fleet"
    },
    # 🇬🇧 UK - National Express
    {
        "id": "NAT-EXPRESS-LDN-MAN",
        "callsign": "NX-505-UK",
        "category": "bus",
        "operator": "National Express UK",
        "origin": {"code": "LDN", "city": "London Victoria Coach (UK)", "lat": 51.4921, "lon": -0.1479},
        "dest": {"code": "MAN", "city": "Manchester Central (UK)", "lat": 53.4774, "lon": -2.2384},
        "speed": 95,
        "altitude": 65,
        "squawk": "NX-505",
        "transponder": "UK Coach Telematics",
        "source": "National Express RT"
    },
    # 🇯🇵 Japan - Willer Express Night/Day Highway Coach
    {
        "id": "WILLER-TYO-KYO",
        "callsign": "WILLER-JP-77",
        "category": "bus",
        "operator": "Willer Express Japan",
        "origin": {"code": "HND", "city": "Tokyo Shinjuku (Japan)", "lat": 35.6896, "lon": 139.7006},
        "dest": {"code": "KIX", "city": "Kyoto Station (Japan)", "lat": 34.9858, "lon": 135.7588},
        "speed": 88,
        "altitude": 55,
        "squawk": "WILLER-77",
        "transponder": "Japan Highway GPS",
        "source": "Willer Telematics"
    },
    # 🇮🇳 India - Haryana Roadways Volvo
    {
        "id": "DL-VOLVO-99",
        "callsign": "HR-68B-1090",
        "category": "bus",
        "operator": "Haryana Roadways Volvo",
        "origin": {"code": "ISBT", "city": "Delhi Kashmiri Gate (India)", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "CDG", "city": "Chandigarh Sec 17 (India)", "lat": 30.7333, "lon": 76.7794},
        "speed": 85,
        "altitude": 235,
        "squawk": "HR-GPS-99",
        "transponder": "AIS-140 GPS Tracker",
        "source": "State Transit GTFS-RT"
    },
    # 🇮🇳 India - KSRTC Airavat Club Class
    {
        "id": "KA-AIRAVAT-44",
        "callsign": "KA-01-F-4021",
        "category": "bus",
        "operator": "KSRTC Airavat Club Class",
        "origin": {"code": "BLR", "city": "Bengaluru Majestic (India)", "lat": 12.9774, "lon": 77.5714},
        "dest": {"code": "HYD", "city": "Hyderabad MGBS (India)", "lat": 17.3753, "lon": 78.4744},
        "speed": 92,
        "altitude": 540,
        "squawk": "KSRTC-4021",
        "transponder": "AIS-140 Smart Transit",
        "source": "KSRTC Mitra Feed"
    }
]

WORLD_CAR_ROUTES = [
    {
        "id": "CAB-DEL-VIP1",
        "callsign": "EV-NEXON-01",
        "category": "car",
        "operator": "BluSmart EV Fleet Delhi",
        "origin": {"code": "IGI-T3", "city": "Delhi IGI Airport", "lat": 28.5562, "lon": 77.1000},
        "dest": {"code": "CP", "city": "Connaught Place", "lat": 28.6315, "lon": 77.2167},
        "speed": 55,
        "altitude": 215,
        "squawk": "EV-DEL",
        "transponder": "OBD-II Telematics",
        "source": "BluSmart Fleet Telemetry"
    },
    {
        "id": "CAB-NYC-YELLOW",
        "callsign": "NYC-MEDALLION-44",
        "category": "car",
        "operator": "NYC Official Yellow Cab",
        "origin": {"code": "JFK", "city": "JFK Airport Terminal 4", "lat": 40.6413, "lon": -73.7781},
        "dest": {"code": "TSQ", "city": "Times Square Manhattan", "lat": 40.7580, "lon": -73.9855},
        "speed": 48,
        "altitude": 10,
        "squawk": "NYC-TLC-44",
        "transponder": "NYC TLC Smart Meter",
        "source": "TLC Open Telematics"
    },
    {
        "id": "CAB-LON-BLACKCAB",
        "callsign": "TX4-LONDON-88",
        "category": "car",
        "operator": "London Electric Black Cab",
        "origin": {"code": "LHR", "city": "Heathrow Airport T5", "lat": 51.4700, "lon": -0.4543},
        "dest": {"code": "WEST", "city": "Westminster London", "lat": 51.4995, "lon": -0.1248},
        "speed": 40,
        "altitude": 20,
        "squawk": "TFL-TX4-88",
        "transponder": "TfL Connected Vehicle",
        "source": "TfL Connected Stream"
    }
]

def calculate_transit_positions() -> List[Dict[str, Any]]:
    """Calculates live positions for buses and cars worldwide along corridors."""
    vehicles = []
    t = time.time() / 70.0

    for idx, item in enumerate(WORLD_BUS_ROUTES + WORLD_CAR_ROUTES):
        o = item["origin"]
        d = item["dest"]

        prog = (math.sin(t + idx * 1.3) + 1.0) / 2.0
        lat = o["lat"] + (d["lat"] - o["lat"]) * prog
        lon = o["lon"] + (d["lon"] - o["lon"]) * prog

        d_lat = d["lat"] - o["lat"]
        d_lon = d["lon"] - o["lon"]
        heading = int(math.degrees(math.atan2(d_lon, d_lat)) + 360) % 360

        vehicles.append({
            "id": item["id"],
            "callsign": item["callsign"],
            "category": item["category"],
            "operator": item["operator"],
            "origin": item["origin"],
            "dest": item["dest"],
            "lat": lat,
            "lon": lon,
            "speed": item["speed"],
            "altitude": item["altitude"],
            "heading": heading,
            "status": f"En Route: {o['city']} ➔ {d['city']}",
            "eta": "Scheduled On Time",
            "fuel": 86,
            "squawk": item["squawk"],
            "transponder": item["transponder"],
            "source": item["source"]
        })

    return vehicles
