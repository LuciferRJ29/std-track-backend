import math
import time
from typing import List, Dict, Any

BUS_ROUTES = [
    {
        "id": "DL-VOLVO-99",
        "callsign": "HR-68B-1090",
        "category": "bus",
        "operator": "Haryana Roadways Volvo",
        "origin": {"code": "ISBT", "city": "Delhi Kashmiri Gate", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "CDG", "city": "Chandigarh Sec 17", "lat": 30.7333, "lon": 76.7794},
        "speed": 85,
        "altitude": 235,
        "squawk": "HR-GPS-99",
        "transponder": "AIS-140 GPS Tracker",
        "source": "State Transit GTFS-RT"
    },
    {
        "id": "KA-AIRAVAT-44",
        "callsign": "KA-01-F-4021",
        "category": "bus",
        "operator": "KSRTC Airavat Club Class",
        "origin": {"code": "BLR", "city": "Bengaluru Majestic", "lat": 12.9774, "lon": 77.5714},
        "dest": {"code": "HYD", "city": "Hyderabad MGBS", "lat": 17.3753, "lon": 78.4744},
        "speed": 92,
        "altitude": 540,
        "squawk": "KSRTC-4021",
        "transponder": "AIS-140 Smart Transit",
        "source": "KSRTC Mitra Feed"
    },
    {
        "id": "MUM-SHIVNERI-12",
        "callsign": "MH-14-BT-3030",
        "category": "bus",
        "operator": "MSRTC Shivneri Volvo",
        "origin": {"code": "DADAR", "city": "Mumbai Dadar", "lat": 19.0178, "lon": 72.8478},
        "dest": {"code": "PUNE", "city": "Pune Swargate", "lat": 18.5018, "lon": 73.8586},
        "speed": 78,
        "altitude": 560,
        "squawk": "MSRTC-3030",
        "transponder": "MSRTC GPS Cloud",
        "source": "State Transit Feed"
    }
]

CAR_ROUTES = [
    {
        "id": "CAB-DEL-VIP1",
        "callsign": "EV-NEXON-01",
        "category": "car",
        "operator": "BluSmart EV Fleet Delhi",
        "origin": {"code": "IGI-T3", "city": "Indira Gandhi Airport", "lat": 28.5562, "lon": 77.1000},
        "dest": {"code": "CP", "city": "Connaught Place", "lat": 28.6315, "lon": 77.2167},
        "speed": 55,
        "altitude": 215,
        "squawk": "EV-FLEET-DEL",
        "transponder": "OBD-II Telematics",
        "source": "BluSmart Fleet Telemetry"
    },
    {
        "id": "CAB-MUM-VIP2",
        "callsign": "UBER-PREM-88",
        "category": "car",
        "operator": "Uber Black Mumbai",
        "origin": {"code": "BKC", "city": "Bandra Kurla Complex", "lat": 19.0657, "lon": 72.8687},
        "dest": {"code": "BOM-T2", "city": "Chhatrapati Shivaji Airport", "lat": 19.0974, "lon": 72.8744},
        "speed": 42,
        "altitude": 12,
        "squawk": "UBR-BKC-88",
        "transponder": "Driver App GPS Stream",
        "source": "Uber Telematics API"
    },
    {
        "id": "CAB-BLR-VIP3",
        "callsign": "OLA-PRIME-09",
        "category": "car",
        "operator": "Ola Electric Cab BLR",
        "origin": {"code": "E-CITY", "city": "Electronic City", "lat": 12.8399, "lon": 77.6770},
        "dest": {"code": "INDIRA", "city": "Indiranagar 100ft Rd", "lat": 12.9784, "lon": 77.6408},
        "speed": 48,
        "altitude": 910,
        "squawk": "OLA-BLR-09",
        "transponder": "Fleet GPS Stream",
        "source": "Ola Fleet Telematics"
    }
]

def calculate_transit_positions() -> List[Dict[str, Any]]:
    """Calculates live positions for buses and fleet vehicles along highway/city corridors."""
    vehicles = []
    t = time.time() / 80.0

    for idx, item in enumerate(BUS_ROUTES + CAR_ROUTES):
        o = item["origin"]
        d = item["dest"]

        # Sinusoidal oscillation along the corridor
        prog = (math.sin(t + idx * 1.5) + 1.0) / 2.0
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
            "status": "Transit Corridor En Route",
            "eta": "12-25 mins",
            "fuel": 84,
            "squawk": item["squawk"],
            "transponder": item["transponder"],
            "source": item["source"]
        })

    return vehicles
