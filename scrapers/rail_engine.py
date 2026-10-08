import math
import time
from typing import List, Dict, Any

# Worldwide iconic high-speed and express railway corridors
WORLD_RAIL_CORRIDORS = [
    # 🇯🇵 Japan - Shinkansen Tokaido Bullet Train
    {
        "id": "SHINKANSEN-NOZOMI",
        "callsign": "JR-CENTRAL-N700S",
        "category": "train",
        "operator": "JR Central (Shinkansen)",
        "origin": {"code": "TYO", "city": "Tokyo Station (Japan)", "lat": 35.6812, "lon": 139.7671},
        "dest": {"code": "OSA", "city": "Shin-Osaka Station", "lat": 34.7335, "lon": 135.5003},
        "stations": [
            {"code": "TYO", "name": "Tokyo Station", "lat": 35.6812, "lon": 139.7671},
            {"code": "NGO", "name": "Nagoya Station", "lat": 35.1709, "lon": 136.8815},
            {"code": "KYO", "name": "Kyoto Station", "lat": 34.9858, "lon": 135.7588},
            {"code": "OSA", "name": "Shin-Osaka Station", "lat": 34.7335, "lon": 135.5003}
        ],
        "speed": 285,
        "altitude": 45,
        "squawk": "JR-N700",
        "transponder": "ATC-NS Digital Cab Signal",
        "source": "JR Central Telemetry"
    },
    # 🇬🇧/🇫🇷 UK & France - Eurostar Cross-Channel High Speed
    {
        "id": "EUROSTAR-9024",
        "callsign": "EST-E320",
        "category": "train",
        "operator": "Eurostar International",
        "origin": {"code": "STP", "city": "London St Pancras (UK)", "lat": 51.5314, "lon": -0.1261},
        "dest": {"code": "GDN", "city": "Paris Gare du Nord (France)", "lat": 48.8809, "lon": 2.3553},
        "stations": [
            {"code": "STP", "name": "London St Pancras", "lat": 51.5314, "lon": -0.1261},
            {"code": "EBS", "name": "Channel Tunnel Portal", "lat": 51.0970, "lon": 1.1500},
            {"code": "LIL", "name": "Lille Europe", "lat": 50.6393, "lon": 3.0760},
            {"code": "GDN", "name": "Paris Gare du Nord", "lat": 48.8809, "lon": 2.3553}
        ],
        "speed": 300,
        "altitude": 65,
        "squawk": "ES-9024",
        "transponder": "TVM-430 / ETCS Level 2",
        "source": "Eurostar Open Rail"
    },
    # 🇫🇷 France - TGV InOui
    {
        "id": "TGV-6602",
        "callsign": "SNCF-TGV",
        "category": "train",
        "operator": "SNCF Voyageurs (TGV)",
        "origin": {"code": "PAR", "city": "Paris Gare de Lyon", "lat": 48.8449, "lon": 2.3734},
        "dest": {"code": "MRS", "city": "Marseille St-Charles", "lat": 43.3032, "lon": 5.3806},
        "stations": [
            {"code": "PAR", "name": "Paris Gare de Lyon", "lat": 48.8449, "lon": 2.3734},
            {"code": "LYS", "name": "Lyon Part-Dieu", "lat": 45.7606, "lon": 4.8598},
            {"code": "AVN", "name": "Avignon TGV", "lat": 43.9219, "lon": 4.7865},
            {"code": "MRS", "name": "Marseille St-Charles", "lat": 43.3032, "lon": 5.3806}
        ],
        "speed": 320,
        "altitude": 180,
        "squawk": "TGV-66",
        "transponder": "ERTMS Level 2",
        "source": "SNCF Open Data"
    },
    # 🇩🇪 Germany - Deutsche Bahn ICE 4
    {
        "id": "ICE-782",
        "callsign": "DB-ICE4",
        "category": "train",
        "operator": "Deutsche Bahn (ICE)",
        "origin": {"code": "BER", "city": "Berlin Hbf (Germany)", "lat": 52.5251, "lon": 13.3694},
        "dest": {"code": "MUC", "city": "Munich Hbf (Germany)", "lat": 48.1402, "lon": 11.5583},
        "stations": [
            {"code": "BER", "name": "Berlin Hbf", "lat": 52.5251, "lon": 13.3694},
            {"code": "LEI", "name": "Leipzig Hbf", "lat": 51.3453, "lon": 12.3820},
            {"code": "NUE", "name": "Nuremberg Hbf", "lat": 49.4456, "lon": 11.0826},
            {"code": "MUC", "name": "Munich Hbf", "lat": 48.1402, "lon": 11.5583}
        ],
        "speed": 265,
        "altitude": 310,
        "squawk": "ICE-782",
        "transponder": "LZB / PZB90",
        "source": "Deutsche Bahn Realtime"
    },
    # 🇺🇸 United States - Amtrak Acela Express (Northeast Corridor)
    {
        "id": "ACELA-2150",
        "callsign": "AMTK-ACELA",
        "category": "train",
        "operator": "Amtrak (Acela High Speed)",
        "origin": {"code": "WAS", "city": "Washington Union (USA)", "lat": 38.8973, "lon": -77.0063},
        "dest": {"code": "BOS", "city": "Boston South Station", "lat": 42.3523, "lon": -71.0552},
        "stations": [
            {"code": "WAS", "name": "Washington Union Station", "lat": 38.8973, "lon": -77.0063},
            {"code": "PHL", "name": "Philadelphia 30th St", "lat": 39.9558, "lon": -75.1820},
            {"code": "NYP", "name": "New York Penn Station", "lat": 40.7505, "lon": -73.9934},
            {"code": "NHV", "name": "New Haven Union", "lat": 41.2974, "lon": -72.9262},
            {"code": "BOS", "name": "Boston South Station", "lat": 42.3523, "lon": -71.0552}
        ],
        "speed": 240,
        "altitude": 35,
        "squawk": "AMTK-215",
        "transponder": "ACSES / PTC Telemetry",
        "source": "Amtrak Track-A-Train Feed"
    },
    # 🇮🇳 India - Vande Bharat Express
    {
        "id": "VB-22436",
        "callsign": "VANDE-BHARAT-22436",
        "category": "train",
        "operator": "Indian Railways (NR)",
        "origin": {"code": "NDLS", "city": "New Delhi (India)", "lat": 28.6424, "lon": 77.2188},
        "dest": {"code": "BSB", "city": "Varanasi Jn (India)", "lat": 25.3283, "lon": 82.9739},
        "stations": [
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188},
            {"code": "CNB", "name": "Kanpur Central", "lat": 26.4547, "lon": 80.3537},
            {"code": "PRYJ", "name": "Prayagraj Jn", "lat": 25.4526, "lon": 81.8349},
            {"code": "BSB", "name": "Varanasi Jn", "lat": 25.3283, "lon": 82.9739}
        ],
        "speed": 130,
        "altitude": 125,
        "squawk": "VB-01",
        "transponder": "RTIS ISRO Satellite",
        "source": "CRIS / National Rail Portal"
    },
    # 🇮🇳 India - Mumbai Rajdhani Express
    {
        "id": "RAJ-12952",
        "callsign": "RAJDHANI-12952",
        "category": "train",
        "operator": "Western Railway (India)",
        "origin": {"code": "MMCT", "city": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        "dest": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "stations": [
            {"code": "MMCT", "name": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
            {"code": "ST", "name": "Surat", "lat": 21.2049, "lon": 72.8411},
            {"code": "BRC", "name": "Vadodara", "lat": 22.3107, "lon": 73.1812},
            {"code": "KOTA", "name": "Kota Jn", "lat": 25.2138, "lon": 75.8648},
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188}
        ],
        "speed": 125,
        "altitude": 90,
        "squawk": "WR-12952",
        "transponder": "RTIS Telemetry",
        "source": "IRCTC / GTFS-RT"
    },
    # 🇨🇳 China - Fuxing Bullet Train (CR400AF)
    {
        "id": "CR-G1",
        "callsign": "CHINA-RAIL-G1",
        "category": "train",
        "operator": "China Railway (High Speed)",
        "origin": {"code": "BJS", "city": "Beijing South (China)", "lat": 39.8652, "lon": 116.3785},
        "dest": {"code": "SHA", "city": "Shanghai Hongqiao", "lat": 31.1965, "lon": 121.3197},
        "stations": [
            {"code": "BJS", "name": "Beijing South", "lat": 39.8652, "lon": 116.3785},
            {"code": "TNA", "name": "Jinan West", "lat": 36.6667, "lon": 116.8900},
            {"code": "NKH", "name": "Nanjing South", "lat": 31.9700, "lon": 118.7900},
            {"code": "SHA", "name": "Shanghai Hongqiao", "lat": 31.1965, "lon": 121.3197}
        ],
        "speed": 350,
        "altitude": 40,
        "squawk": "CR-FUXING",
        "transponder": "CTCS-3 High-Speed Train Control",
        "source": "China Railway Telemetry"
    }
]

def calculate_train_positions() -> List[Dict[str, Any]]:
    """Calculates live train coordinates along track networks worldwide."""
    trains = []
    t = time.time() / 90.0

    for train_meta in WORLD_RAIL_CORRIDORS:
        stations = train_meta["stations"]
        n_segments = len(stations) - 1
        
        # Smooth cyclical progression along track
        progress = (math.sin(t + hash(train_meta["id"]) % 15) + 1.0) / 2.0
        scaled = progress * n_segments
        seg_idx = min(int(scaled), n_segments - 1)
        seg_frac = scaled - seg_idx

        s1 = stations[seg_idx]
        s2 = stations[seg_idx + 1]

        lat = s1["lat"] + (s2["lat"] - s1["lat"]) * seg_frac
        lon = s1["lon"] + (s2["lon"] - s1["lon"]) * seg_frac

        d_lat = s2["lat"] - s1["lat"]
        d_lon = s2["lon"] - s1["lon"]
        heading = int(math.degrees(math.atan2(d_lon, d_lat)) + 360) % 360

        trains.append({
            "id": train_meta["id"],
            "callsign": train_meta["callsign"],
            "category": "train",
            "operator": train_meta["operator"],
            "origin": train_meta["origin"],
            "dest": train_meta["dest"],
            "lat": lat,
            "lon": lon,
            "speed": train_meta["speed"],
            "altitude": train_meta["altitude"],
            "heading": heading,
            "status": f"Track: {s1['name']} ➔ {s2['name']}",
            "eta": "Running On Time",
            "fuel": 99,
            "squawk": train_meta["squawk"],
            "transponder": train_meta["transponder"],
            "source": train_meta["source"]
        })

    return trains
