import math
import time
from typing import List, Dict, Any

WORLD_BUS_ROUTES = [
    # 🇮🇳 INDIA - Haryana Roadways Volvo
    {
        "id": "HR-VOLVO-99", "callsign": "HR-68B-1090", "category": "bus",
        "operator": "Haryana Roadways Super Luxury",
        "origin": {"code": "DEL-ISBT", "city": "Delhi Kashmiri Gate", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "CHD-17", "city": "Chandigarh Sec 17", "lat": 30.7333, "lon": 76.7794},
        "speed": 85, "altitude": 235, "squawk": "HR-GPS-99", "transponder": "AIS-140 GPS Tracker", "source": "State Roadways Telematics"
    },
    # 🇮🇳 INDIA - HRTC Himsuta Volvo (Delhi - Manali)
    {
        "id": "HRTC-HIMSUTA-04", "callsign": "HP-63A-4040", "category": "bus",
        "operator": "HRTC Himsuta Luxury",
        "origin": {"code": "DEL-ISBT", "city": "Delhi Kashmiri Gate", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "MANALI", "city": "Manali Mall Road", "lat": 32.2396, "lon": 77.1887},
        "speed": 75, "altitude": 1150, "squawk": "HRTC-04", "transponder": "AIS-140 Hill Highway GPS", "source": "HRTC Live Fleet"
    },
    # 🇮🇳 INDIA - HRTC Himgaura (Delhi - Dharamshala)
    {
        "id": "HRTC-HIMGAURA-18", "callsign": "HP-68-1818", "category": "bus",
        "operator": "HRTC Himgaura AC",
        "origin": {"code": "DEL-ISBT", "city": "Delhi Kashmiri Gate", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "DHRM", "city": "Dharamshala Kotwali", "lat": 32.2190, "lon": 76.3234},
        "speed": 70, "altitude": 1450, "squawk": "HRTC-18", "transponder": "AIS-140 GPS", "source": "HRTC Telematics"
    },
    # 🇮🇳 INDIA - RSRTC Goldline (Delhi - Jaipur)
    {
        "id": "RSRTC-JAIPUR-21", "callsign": "RJ-14-PC-2121", "category": "bus",
        "operator": "RSRTC Super Goldline AC",
        "origin": {"code": "DEL-BH", "city": "Delhi Bikaner House", "lat": 28.6083, "lon": 77.2366},
        "dest": {"code": "JAI-SC", "city": "Jaipur Sindhi Camp", "lat": 26.9196, "lon": 75.7981},
        "speed": 80, "altitude": 430, "squawk": "RSRTC-21", "transponder": "RSRTC Fleet Tracker", "source": "Rajasthan Roadways RT"
    },
    # 🇮🇳 INDIA - RSRTC Marwar Volvo (Jaipur - Jodhpur)
    {
        "id": "RSRTC-MARWAR-08", "callsign": "RJ-19-PA-0808", "category": "bus",
        "operator": "RSRTC Volvo Superfast",
        "origin": {"code": "JAI-SC", "city": "Jaipur Sindhi Camp", "lat": 26.9196, "lon": 75.7981},
        "dest": {"code": "JDH-BS", "city": "Jodhpur Raika Bagh", "lat": 26.2918, "lon": 73.0360},
        "speed": 85, "altitude": 240, "squawk": "RSRTC-08", "transponder": "RSRTC GPS", "source": "Rajasthan Roadways RT"
    },
    # 🇮🇳 INDIA - UPSRTC Janrath AC (Delhi - Agra - Lucknow)
    {
        "id": "UPSRTC-JANRATH-55", "callsign": "UP-32-JN-5555", "category": "bus",
        "operator": "UPSRTC Janrath AC Express",
        "origin": {"code": "DEL-AV", "city": "Delhi Anand Vihar ISBT", "lat": 28.6469, "lon": 77.3164},
        "dest": {"code": "LKO-CB", "city": "Lucknow Charbagh", "lat": 26.8322, "lon": 80.9189},
        "speed": 90, "altitude": 140, "squawk": "UPSRTC-55", "transponder": "AIS-140 Expressway GPS", "source": "Yamuna Expressway Telematics"
    },
    # 🇮🇳 INDIA - UPSRTC Royal Cruiser Scania (Delhi - Varanasi)
    {
        "id": "UPSRTC-SCANIA-88", "callsign": "UP-65-RC-8888", "category": "bus",
        "operator": "UPSRTC Royal Cruiser Scania",
        "origin": {"code": "DEL-AV", "city": "Delhi Anand Vihar", "lat": 28.6469, "lon": 77.3164},
        "dest": {"code": "BSB-CB", "city": "Varanasi Cantt ISBT", "lat": 25.3283, "lon": 82.9800},
        "speed": 88, "altitude": 95, "squawk": "UPSRTC-88", "transponder": "AIS-140 GPS", "source": "Purvanchal Expressway Telematics"
    },
    # 🇮🇳 INDIA - MSRTC Shivneri Scania (Mumbai - Pune)
    {
        "id": "MSRTC-SHIVNERI-18", "callsign": "MH-14-BT-1818", "category": "bus",
        "operator": "MSRTC Shivneri Luxury",
        "origin": {"code": "MUM-DADAR", "city": "Mumbai Dadar", "lat": 19.0178, "lon": 72.8478},
        "dest": {"code": "PUN-STN", "city": "Pune Railway Station", "lat": 18.5289, "lon": 73.8744},
        "speed": 82, "altitude": 560, "squawk": "MSRTC-18", "transponder": "Mumbai-Pune Expressway Telematics", "source": "MSRTC Live Transit"
    },
    # 🇮🇳 INDIA - MSRTC Shivshahi AC (Pune - Kolhapur)
    {
        "id": "MSRTC-SHIVSHAHI-44", "callsign": "MH-09-SS-4444", "category": "bus",
        "operator": "MSRTC Shivshahi AC",
        "origin": {"code": "PUN-SWAR", "city": "Pune Swargate", "lat": 18.5018, "lon": 73.8580},
        "dest": {"code": "KOP-CBS", "city": "Kolhapur Central Bus Stand", "lat": 16.7050, "lon": 74.2433},
        "speed": 78, "altitude": 580, "squawk": "MSRTC-44", "transponder": "AIS-140 GPS", "source": "MSRTC Telematics"
    },
    # 🇮🇳 INDIA - KSRTC Airavat Club Class (Bengaluru - Mysuru)
    {
        "id": "KSRTC-AIRAVAT-77", "callsign": "KA-57-F-7777", "category": "bus",
        "operator": "KSRTC Airavat Multi-Axle Volvo",
        "origin": {"code": "BLR-MAJ", "city": "Bengaluru Kempegowda Majestic", "lat": 12.9772, "lon": 77.5713},
        "dest": {"code": "MYS-SUB", "city": "Mysuru Suburb Bus Stand", "lat": 12.3072, "lon": 76.6558},
        "speed": 85, "altitude": 820, "squawk": "KSRTC-77", "transponder": "Bengaluru-Mysuru Expressway ITS", "source": "KSRTC Live Feed"
    },
    # 🇮🇳 INDIA - KSRTC Flybus (Bengaluru Airport - Mysuru)
    {
        "id": "KSRTC-FLYBUS-01", "callsign": "KA-57-FB-0101", "category": "bus",
        "operator": "KSRTC Flybus Premium",
        "origin": {"code": "BLR-KIA", "city": "Bengaluru Airport KIA T2", "lat": 13.1986, "lon": 77.7066},
        "dest": {"code": "MYS-SUB", "city": "Mysuru Suburb Bus Stand", "lat": 12.3072, "lon": 76.6558},
        "speed": 88, "altitude": 850, "squawk": "FLYBUS-01", "transponder": "Airport Express GPS", "source": "KSRTC Telematics"
    },
    # 🇮🇳 INDIA - TSRTC Garuda Plus (Hyderabad - Vijayawada)
    {
        "id": "TSRTC-GARUDA-33", "callsign": "TS-09-Z-3333", "category": "bus",
        "operator": "TSRTC Garuda Plus AC",
        "origin": {"code": "HYD-MGBS", "city": "Hyderabad MGBS", "lat": 17.3789, "lon": 78.4800},
        "dest": {"code": "VJA-PNBS", "city": "Vijayawada PNBS", "lat": 16.5062, "lon": 80.6480},
        "speed": 82, "altitude": 320, "squawk": "TSRTC-33", "transponder": "AIS-140 GPS", "source": "TSRTC Live"
    },
    # 🇮🇳 INDIA - SETC Ultra Deluxe AC (Chennai - Madurai)
    {
        "id": "SETC-ULTRA-50", "callsign": "TN-01-AN-5050", "category": "bus",
        "operator": "SETC Tamil Nadu AC Sleeper",
        "origin": {"code": "MAA-CMBT", "city": "Chennai Koyambedu CMBT", "lat": 13.0694, "lon": 80.2056},
        "dest": {"code": "MDU-MAT", "city": "Madurai Mattuthavani", "lat": 9.9400, "lon": 78.1500},
        "speed": 80, "altitude": 140, "squawk": "SETC-50", "transponder": "TN Transport ITS", "source": "SETC Telematics"
    },
    # 🇮🇳 INDIA - GSRTC Gurjanagari (Ahmedabad - Surat)
    {
        "id": "GSRTC-GURJARA-88", "callsign": "GJ-18-Z-8888", "category": "bus",
        "operator": "GSRTC Gurjanagari Express",
        "origin": {"code": "ADI-GM", "city": "Ahmedabad Gita Mandir", "lat": 23.0120, "lon": 72.5950},
        "dest": {"code": "ST-CBS", "city": "Surat Central Bus Station", "lat": 21.2000, "lon": 72.8400},
        "speed": 80, "altitude": 45, "squawk": "GSRTC-88", "transponder": "GSRTC GPS", "source": "Gujarat State Transport"
    },
    # 🇮🇳 INDIA - NueGo Electric Intercity (Delhi - Agra Expressway)
    {
        "id": "NUEGO-EV-01", "callsign": "DL-1V-EV-0101", "category": "bus",
        "operator": "NueGo 100% Electric Intercity",
        "origin": {"code": "DEL-ISBT", "city": "Delhi Kashmiri Gate", "lat": 28.6675, "lon": 77.2330},
        "dest": {"code": "AGRA-ISBT", "city": "Agra ISBT Transport Nagar", "lat": 27.2000, "lon": 77.9700},
        "speed": 85, "altitude": 170, "squawk": "NUEGO-EV-01", "transponder": "EV Smart Telematics (Battery 78%)", "source": "NueGo Fleet Cloud"
    },

    # 🇺🇸 USA - Greyhound & FlixBus
    {
        "id": "GREYHOUND-NYC-DC", "callsign": "GH-US-101", "category": "bus",
        "operator": "Greyhound Express Lines",
        "origin": {"code": "PABT", "city": "New York Port Authority", "lat": 40.7570, "lon": -73.9904},
        "dest": {"code": "WAS-US", "city": "Washington DC Union Station", "lat": 38.8973, "lon": -77.0063},
        "speed": 95, "altitude": 25, "squawk": "GH-101", "transponder": "FMCSA Connected GPS", "source": "Greyhound Telematics"
    },
    {
        "id": "FLIXBUS-LA-SD", "callsign": "FLIX-CA-504", "category": "bus",
        "operator": "FlixBus USA West Coast",
        "origin": {"code": "LAX-DT", "city": "Los Angeles Downtown", "lat": 34.0522, "lon": -118.2437},
        "dest": {"code": "SAN-DT", "city": "San Diego Santa Fe Depot", "lat": 32.7157, "lon": -117.1611},
        "speed": 100, "altitude": 40, "squawk": "FLIX-504", "transponder": "Flix Fleet Tracker", "source": "FlixBus Real-Time API"
    },

    # 🇪🇺 EUROPE - FlixBus Europe
    {
        "id": "FLIXBUS-BERLIN-PRAGUE", "callsign": "FLIX-EU-012", "category": "bus",
        "operator": "FlixBus DACH Europe",
        "origin": {"code": "BER-ZOB", "city": "Berlin Central ZOB", "lat": 52.5072, "lon": 13.2798},
        "dest": {"code": "PRG-FLO", "city": "Prague Florenc Central Bus", "lat": 50.0898, "lon": 14.4411},
        "speed": 98, "altitude": 210, "squawk": "FLIX-012", "transponder": "EU Fleet IoT", "source": "FlixMobility API"
    },
    {
        "id": "FLIXBUS-PARIS-AMSTERDAM", "callsign": "FLIX-EU-330", "category": "bus",
        "operator": "FlixBus West Europe",
        "origin": {"code": "PAR-BERCY", "city": "Paris Bercy Seine", "lat": 48.8352, "lon": 2.3789},
        "dest": {"code": "AMS-SLOT", "city": "Amsterdam Sloterdijk", "lat": 52.3888, "lon": 4.8378},
        "speed": 95, "altitude": 35, "squawk": "FLIX-330", "transponder": "EU Fleet IoT", "source": "FlixMobility API"
    }
]

WORLD_CAR_ROUTES = [
    # 🇮🇳 INDIA - BluSmart EV Intercity
    {
        "id": "BLUSMART-DEL-GUR", "callsign": "BLU-EV-DEL-01", "category": "car",
        "operator": "BluSmart All-Electric Fleet",
        "origin": {"code": "DEL-CP", "city": "Delhi Connaught Place", "lat": 28.6315, "lon": 77.2167},
        "dest": {"code": "GUR-CYB", "city": "Gurugram Cyber Hub", "lat": 28.4986, "lon": 77.0878},
        "speed": 55, "altitude": 215, "squawk": "BLU-EV-01", "transponder": "EV Telematics (Battery 82%)", "source": "BluSmart Telematics"
    },
    # 🇮🇳 INDIA - Mumbai Sea Link Taxi
    {
        "id": "TAXI-MUMBAI-BWSL", "callsign": "MH-01-TAXI-99", "category": "car",
        "operator": "Mumbai Premier Cool Cab",
        "origin": {"code": "WORLI", "city": "Worli Sea Face Mumbai", "lat": 19.0100, "lon": 72.8150},
        "dest": {"code": "BANDRA", "city": "Bandra Kurla Complex (BKC)", "lat": 19.0600, "lon": 72.8650},
        "speed": 65, "altitude": 15, "squawk": "MUM-CC-99", "transponder": "GPS Smart Taxi Meter", "source": "Mumbai RTO Fleet"
    },
    # 🇺🇸 USA - NYC Yellow Cab
    {
        "id": "CAB-NYC-YELLOW", "callsign": "NYC-MEDALLION-44", "category": "car",
        "operator": "NYC Official Yellow Cab",
        "origin": {"code": "JFK", "city": "JFK Airport Terminal 4", "lat": 40.6413, "lon": -73.7781},
        "dest": {"code": "TSQ", "city": "Times Square Manhattan", "lat": 40.7580, "lon": -73.9855},
        "speed": 48, "altitude": 10, "squawk": "NYC-TLC-44", "transponder": "NYC TLC Smart Meter", "source": "TLC Open Telematics"
    }
]

def calculate_transit_positions() -> List[Dict[str, Any]]:
    """Calculates live positions for buses and cars worldwide along corridors."""
    vehicles = []
    t = time.time() / 65.0

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
