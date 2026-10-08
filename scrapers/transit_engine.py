import math
import time
from typing import List, Dict, Any

WORLD_BUS_ROUTES = [
    # 🇮🇳 INDIA - Haryana Roadways Volvo
    {
        "id": "HR-VOLVO-99",
        "callsign": "HR-68B-1090",
        "category": "bus",
        "operator": "Haryana Roadways Super Luxury",
        "origin": {"code": "DEL-ISBT", "city": "Delhi Kashmiri Gate (India)", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "CHD-17", "city": "Chandigarh Sec 17 (India)", "lat": 30.7333, "lon": 76.7794},
        "speed": 85,
        "altitude": 235,
        "squawk": "HR-GPS-99",
        "transponder": "AIS-140 GPS Tracker",
        "source": "State Roadways Telematics"
    },
    # 🇮🇳 INDIA - HRTC Himsuta Volvo (Delhi - Manali)
    {
        "id": "HRTC-HIMSUTA-04",
        "callsign": "HP-63A-4040",
        "category": "bus",
        "operator": "HRTC Himsuta Luxury",
        "origin": {"code": "DEL-ISBT", "city": "Delhi Kashmiri Gate (India)", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "MANALI", "city": "Manali Mall Road (India)", "lat": 32.2396, "lon": 77.1887},
        "speed": 75,
        "altitude": 1150,
        "squawk": "HRTC-04",
        "transponder": "AIS-140 Hill Highway GPS",
        "source": "HRTC Live Fleet"
    },
    # 🇮🇳 INDIA - RSRTC Goldline (Delhi - Jaipur)
    {
        "id": "RSRTC-JAIPUR-21",
        "callsign": "RJ-14-PC-2121",
        "category": "bus",
        "operator": "RSRTC Super Goldline AC",
        "origin": {"code": "DEL-BH", "city": "Delhi Bikaner House (India)", "lat": 28.6083, "lon": 77.2366},
        "dest": {"code": "JAI-SC", "city": "Jaipur Sindhi Camp (India)", "lat": 26.9196, "lon": 75.7981},
        "speed": 80,
        "altitude": 430,
        "squawk": "RSRTC-21",
        "transponder": "RSRTC Fleet Tracker",
        "source": "Rajasthan Roadways RT"
    },
    # 🇮🇳 INDIA - UPSRTC Janrath AC (Delhi - Agra - Lucknow)
    {
        "id": "UPSRTC-JANRATH-55",
        "callsign": "UP-32-JN-5555",
        "category": "bus",
        "operator": "UPSRTC Janrath AC Express",
        "origin": {"code": "DEL-AV", "city": "Delhi Anand Vihar ISBT (India)", "lat": 28.6469, "lon": 77.3164},
        "dest": {"code": "LKO-CB", "city": "Lucknow Charbagh (India)", "lat": 26.8322, "lon": 80.9189},
        "speed": 90,
        "altitude": 140,
        "squawk": "UPSRTC-55",
        "transponder": "AIS-140 Expressway GPS",
        "source": "Yamuna Expressway Telematics"
    },
    # 🇮🇳 INDIA - MSRTC Shivneri Scania (Mumbai - Pune)
    {
        "id": "MSRTC-SHIVNERI-18",
        "callsign": "MH-14-BT-1818",
        "category": "bus",
        "operator": "MSRTC Shivneri Luxury",
        "origin": {"code": "MUM-DADAR", "city": "Mumbai Dadar (India)", "lat": 19.0178, "lon": 72.8478},
        "dest": {"code": "PUN-STN", "city": "Pune Railway Station (India)", "lat": 18.5289, "lon": 73.8744},
        "speed": 82,
        "altitude": 560,
        "squawk": "MSRTC-18",
        "transponder": "Expressway Smart GPS",
        "source": "MSRTC Live Mitra"
    },
    # 🇮🇳 INDIA - KSRTC Airavat Club Class (Bengaluru - Hyderabad)
    {
        "id": "KSRTC-AIRAVAT-77",
        "callsign": "KA-01-F-7777",
        "category": "bus",
        "operator": "KSRTC Airavat Multi-Axle",
        "origin": {"code": "BLR-MAJ", "city": "Bengaluru Majestic (India)", "lat": 12.9774, "lon": 77.5714},
        "dest": {"code": "HYD-MGBS", "city": "Hyderabad MGBS (India)", "lat": 17.3753, "lon": 78.4744},
        "speed": 92,
        "altitude": 540,
        "squawk": "KSRTC-77",
        "transponder": "AIS-140 Smart Transit",
        "source": "KSRTC Mitra Live Feed"
    },
    # 🇮🇳 INDIA - KSRTC Ambaari Dream Class (Bengaluru - Chennai)
    {
        "id": "KSRTC-AMBAARI-33",
        "callsign": "KA-57-F-3333",
        "category": "bus",
        "operator": "KSRTC Ambaari Sleeper",
        "origin": {"code": "BLR-SHANTI", "city": "Bengaluru Shantinagar (India)", "lat": 12.9536, "lon": 77.5954},
        "dest": {"code": "MAA-CMBT", "city": "Chennai CMBT Koyambedu (India)", "lat": 13.0694, "lon": 80.2057},
        "speed": 88,
        "altitude": 120,
        "squawk": "KSRTC-33",
        "transponder": "Smart Sleeper Telematics",
        "source": "KSRTC Mitra Live Feed"
    },
    # 🇮🇳 INDIA - GSRTC Volvo (Ahmedabad - Surat - Mumbai)
    {
        "id": "GSRTC-VOLVO-88",
        "callsign": "GJ-18-Z-8888",
        "category": "bus",
        "operator": "GSRTC Gurjarnagari Volvo",
        "origin": {"code": "ADI-GM", "city": "Ahmedabad Geeta Mandir (India)", "lat": 23.0130, "lon": 72.5930},
        "dest": {"code": "MUM-BORIVLI", "city": "Mumbai Borivali (India)", "lat": 19.2288, "lon": 72.8541},
        "speed": 85,
        "altitude": 45,
        "squawk": "GSRTC-88",
        "transponder": "Gujarat Roadways GPS",
        "source": "GSRTC Live Transit"
    },
    # 🇺🇸 USA - Greyhound Express (New York - Boston)
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
    # 🇺🇸 USA - Greyhound California (LA - San Francisco)
    {
        "id": "GREYHOUND-LA-SF",
        "callsign": "GH-2088-CA",
        "category": "bus",
        "operator": "Greyhound California",
        "origin": {"code": "LAX", "city": "Los Angeles Union (USA)", "lat": 34.0562, "lon": -118.2365},
        "dest": {"code": "SFO", "city": "San Francisco Transbay (USA)", "lat": 37.7897, "lon": -122.3969},
        "speed": 110,
        "altitude": 85,
        "squawk": "GH-US-02",
        "transponder": "ELD GPS Stream",
        "source": "US Interstate Telematics"
    },
    # 🇪🇺 EUROPE - FlixBus (Paris - Brussels - Amsterdam)
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
    # 🇬🇧 UK - National Express (London - Manchester)
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
    }
]

WORLD_CAR_ROUTES = [
    # 🇮🇳 India - Delhi BluSmart EV Fleet
    {
        "id": "BLUSMART-DEL-01",
        "callsign": "DL-1EV-1001",
        "category": "car",
        "operator": "BluSmart EV Fleet Delhi",
        "origin": {"code": "IGI-T3", "city": "Delhi IGI Airport T3", "lat": 28.5562, "lon": 77.1000},
        "dest": {"code": "CP", "city": "Connaught Place Delhi", "lat": 28.6315, "lon": 77.2167},
        "speed": 55,
        "altitude": 215,
        "squawk": "BLU-DEL-01",
        "transponder": "OBD-II EV Telematics",
        "source": "BluSmart Fleet Telemetry"
    },
    # 🇮🇳 India - Delhi NCR Intercity EV
    {
        "id": "BLUSMART-NCR-02",
        "callsign": "HR-26EV-2002",
        "category": "car",
        "operator": "BluSmart EV Fleet Gurugram",
        "origin": {"code": "CYBER-HUB", "city": "Gurugram Cyber Hub", "lat": 28.4950, "lon": 77.0895},
        "dest": {"code": "NOIDA-62", "city": "Noida Sector 62", "lat": 28.6280, "lon": 77.3649},
        "speed": 60,
        "altitude": 220,
        "squawk": "BLU-NCR-02",
        "transponder": "OBD-II Telematics",
        "source": "BluSmart Fleet Telemetry"
    },
    # 🇮🇳 India - Mumbai Uber Black
    {
        "id": "UBER-MUM-PREM",
        "callsign": "MH-02-UB-8888",
        "category": "car",
        "operator": "Uber Black Mumbai",
        "origin": {"code": "BKC", "city": "Bandra Kurla Complex", "lat": 19.0657, "lon": 72.8687},
        "dest": {"code": "BOM-T2", "city": "Mumbai CSIA Airport T2", "lat": 19.0974, "lon": 72.8744},
        "speed": 45,
        "altitude": 15,
        "squawk": "UBR-MUM-88",
        "transponder": "Driver App Live GPS",
        "source": "Uber Telematics API"
    },
    # 🇮🇳 India - Bengaluru Ola Electric
    {
        "id": "OLA-BLR-ELEC",
        "callsign": "KA-03-OL-9999",
        "category": "car",
        "operator": "Ola Electric Bengaluru",
        "origin": {"code": "ECITY", "city": "Electronic City Phase 1", "lat": 12.8399, "lon": 77.6770},
        "dest": {"code": "INDIRA", "city": "Indiranagar 100ft Road", "lat": 12.9784, "lon": 77.6408},
        "speed": 48,
        "altitude": 910,
        "squawk": "OLA-BLR-99",
        "transponder": "Connected Fleet IoT",
        "source": "Ola Telematics Feed"
    },
    # 🇺🇸 USA - NYC Yellow Cab
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
