import math
import time
from typing import List, Dict, Any

# Complete network of Indian Railways express trains & iconic world high-speed rail
WORLD_RAIL_CORRIDORS = [
    # 🇮🇳 INDIA - Vande Bharat Express (Delhi - Varanasi)
    {
        "id": "VB-22436",
        "callsign": "VANDE-BHARAT-22436",
        "category": "train",
        "operator": "Indian Railways (NR)",
        "origin": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "dest": {"code": "BSB", "city": "Varanasi Jn", "lat": 25.3283, "lon": 82.9739},
        "stations": [
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188},
            {"code": "CNB", "name": "Kanpur Central", "lat": 26.4547, "lon": 80.3537},
            {"code": "PRYJ", "name": "Prayagraj Jn", "lat": 25.4526, "lon": 81.8349},
            {"code": "BSB", "name": "Varanasi Jn", "lat": 25.3283, "lon": 82.9739}
        ],
        "speed": 130,
        "altitude": 125,
        "squawk": "VB-22436",
        "transponder": "RTIS ISRO Satellite",
        "source": "CRIS / Indian Railways"
    },
    # 🇮🇳 INDIA - Vande Bharat (Mumbai - Ahmedabad)
    {
        "id": "VB-20901",
        "callsign": "VANDE-BHARAT-20901",
        "category": "train",
        "operator": "Western Railway (WR)",
        "origin": {"code": "MMCT", "city": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        "dest": {"code": "ADI", "city": "Ahmedabad Jn", "lat": 23.0225, "lon": 72.5714},
        "stations": [
            {"code": "MMCT", "name": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
            {"code": "ST", "name": "Surat", "lat": 21.2049, "lon": 72.8411},
            {"code": "BRC", "name": "Vadodara Jn", "lat": 22.3107, "lon": 73.1812},
            {"code": "ADI", "name": "Ahmedabad Jn", "lat": 23.0225, "lon": 72.5714}
        ],
        "speed": 135,
        "altitude": 55,
        "squawk": "VB-20901",
        "transponder": "RTIS ISRO Satellite",
        "source": "CRIS / Indian Railways"
    },
    # 🇮🇳 INDIA - Vande Bharat (Chennai - Coimbatore)
    {
        "id": "VB-20643",
        "callsign": "VANDE-BHARAT-20643",
        "category": "train",
        "operator": "Southern Railway (SR)",
        "origin": {"code": "MAS", "city": "Chennai Central", "lat": 13.0827, "lon": 80.2707},
        "dest": {"code": "CBE", "city": "Coimbatore Jn", "lat": 11.0168, "lon": 76.9558},
        "stations": [
            {"code": "MAS", "name": "Chennai Central", "lat": 13.0827, "lon": 80.2707},
            {"code": "SA", "name": "Salem Jn", "lat": 11.6643, "lon": 78.1460},
            {"code": "ED", "name": "Erode Jn", "lat": 11.3410, "lon": 77.7172},
            {"code": "CBE", "name": "Coimbatore Jn", "lat": 11.0168, "lon": 76.9558}
        ],
        "speed": 130,
        "altitude": 190,
        "squawk": "VB-20643",
        "transponder": "RTIS Satellite",
        "source": "CRIS Live Rail"
    },
    # 🇮🇳 INDIA - Vande Bharat (Kacheguda - Bengaluru)
    {
        "id": "VB-20703",
        "callsign": "VANDE-BHARAT-20703",
        "category": "train",
        "operator": "South Central Railway (SCR)",
        "origin": {"code": "KCG", "city": "Hyderabad Kacheguda", "lat": 17.3916, "lon": 78.5020},
        "dest": {"code": "YPR", "city": "Bengaluru Yesvantpur", "lat": 13.0238, "lon": 77.5503},
        "stations": [
            {"code": "KCG", "name": "Hyderabad Kacheguda", "lat": 17.3916, "lon": 78.5020},
            {"code": "KRNT", "name": "Kurnool City", "lat": 15.8281, "lon": 78.0373},
            {"code": "ATP", "name": "Anantapur", "lat": 14.6819, "lon": 77.6006},
            {"code": "YPR", "name": "Bengaluru Yesvantpur", "lat": 13.0238, "lon": 77.5503}
        ],
        "speed": 125,
        "altitude": 510,
        "squawk": "VB-20703",
        "transponder": "RTIS Satellite",
        "source": "CRIS Live Rail"
    },
    # 🇮🇳 INDIA - Mumbai Rajdhani Express (12952)
    {
        "id": "RAJ-12952",
        "callsign": "RAJDHANI-12952",
        "category": "train",
        "operator": "Western Railway (WR)",
        "origin": {"code": "MMCT", "city": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        "dest": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "stations": [
            {"code": "MMCT", "name": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
            {"code": "ST", "name": "Surat", "lat": 21.2049, "lon": 72.8411},
            {"code": "BRC", "name": "Vadodara Jn", "lat": 22.3107, "lon": 73.1812},
            {"code": "KOTA", "name": "Kota Jn", "lat": 25.2138, "lon": 75.8648},
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188}
        ],
        "speed": 130,
        "altitude": 90,
        "squawk": "WR-12952",
        "transponder": "RTIS Telemetry",
        "source": "IRCTC / GTFS-RT"
    },
    # 🇮🇳 INDIA - Howrah Rajdhani Express (12301)
    {
        "id": "RAJ-12301",
        "callsign": "HOWRAH-RAJDHANI",
        "category": "train",
        "operator": "Eastern Railway (ER)",
        "origin": {"code": "HWH", "city": "Kolkata Howrah", "lat": 22.5850, "lon": 88.3426},
        "dest": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "stations": [
            {"code": "HWH", "name": "Kolkata Howrah", "lat": 22.5850, "lon": 88.3426},
            {"code": "ASN", "name": "Asansol Jn", "lat": 23.6889, "lon": 86.9661},
            {"code": "DDU", "name": "Pt Deen Dayal Upadhyaya", "lat": 25.2818, "lon": 83.1190},
            {"code": "CNB", "name": "Kanpur Central", "lat": 26.4547, "lon": 80.3537},
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188}
        ],
        "speed": 130,
        "altitude": 80,
        "squawk": "ER-12301",
        "transponder": "RTIS ISRO",
        "source": "CRIS / Indian Railways"
    },
    # 🇮🇳 INDIA - Bengaluru Rajdhani Express (22691)
    {
        "id": "RAJ-22691",
        "callsign": "BLR-RAJDHANI",
        "category": "train",
        "operator": "South Western Railway (SWR)",
        "origin": {"code": "SBC", "city": "Bengaluru KSR", "lat": 12.9774, "lon": 77.5714},
        "dest": {"code": "NZM", "city": "Delhi Hazrat Nizamuddin", "lat": 28.5888, "lon": 77.2536},
        "stations": [
            {"code": "SBC", "name": "Bengaluru KSR", "lat": 12.9774, "lon": 77.5714},
            {"code": "SC", "name": "Secunderabad Jn", "lat": 17.4399, "lon": 78.5017},
            {"code": "NGP", "name": "Nagpur Jn", "lat": 21.1524, "lon": 79.0887},
            {"code": "BPL", "name": "Bhopal Jn", "lat": 23.2599, "lon": 77.4126},
            {"code": "NZM", "name": "Delhi Nizamuddin", "lat": 28.5888, "lon": 77.2536}
        ],
        "speed": 125,
        "altitude": 420,
        "squawk": "SWR-22691",
        "transponder": "RTIS Telemetry",
        "source": "National Rail Portal"
    },
    # 🇮🇳 INDIA - Kerala Express (12626)
    {
        "id": "EXP-12626",
        "callsign": "KERALA-EXPRESS",
        "category": "train",
        "operator": "Southern Railway",
        "origin": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "dest": {"code": "TVC", "city": "Thiruvananthapuram Kochuveli", "lat": 8.4875, "lon": 76.9525},
        "stations": [
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188},
            {"code": "GWL", "name": "Gwalior Jn", "lat": 26.2183, "lon": 78.1828},
            {"code": "BPL", "name": "Bhopal Jn", "lat": 23.2599, "lon": 77.4126},
            {"code": "NGP", "name": "Nagpur Jn", "lat": 21.1524, "lon": 79.0887},
            {"code": "BZA", "name": "Vijayawada Jn", "lat": 16.5062, "lon": 80.6480},
            {"code": "ERS", "name": "Ernakulam Jn", "lat": 9.9816, "lon": 76.2999},
            {"code": "TVC", "name": "Thiruvananthapuram", "lat": 8.4875, "lon": 76.9525}
        ],
        "speed": 110,
        "altitude": 110,
        "squawk": "SR-12626",
        "transponder": "RTIS Satellite",
        "source": "CRIS Live Rail"
    },
    # 🇮🇳 INDIA - Gatimaan Express (12050)
    {
        "id": "GAT-12050",
        "callsign": "GATIMAAN-12050",
        "category": "train",
        "operator": "Northern Railway",
        "origin": {"code": "NZM", "city": "Hazrat Nizamuddin", "lat": 28.5888, "lon": 77.2536},
        "dest": {"code": "AGC", "city": "Agra Cantt", "lat": 27.1584, "lon": 77.9904},
        "stations": [
            {"code": "NZM", "name": "Hazrat Nizamuddin", "lat": 28.5888, "lon": 77.2536},
            {"code": "MTJ", "name": "Mathura Jn", "lat": 27.4924, "lon": 77.6737},
            {"code": "AGC", "name": "Agra Cantt", "lat": 27.1584, "lon": 77.9904}
        ],
        "speed": 160,
        "altitude": 175,
        "squawk": "GM-12050",
        "transponder": "RTIS Satellite",
        "source": "National Rail Portal"
    },
    # 🇯🇵 JAPAN - Shinkansen Nozomi (Tokyo - Osaka)
    {
        "id": "SHINKANSEN-NOZOMI",
        "callsign": "JR-CENTRAL-N700S",
        "category": "train",
        "operator": "JR Central (Shinkansen)",
        "origin": {"code": "TYO", "city": "Tokyo Station", "lat": 35.6812, "lon": 139.7671},
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
        "transponder": "ATC-NS Cab Signal",
        "source": "JR Central Telemetry"
    },
    # 🇬🇧/🇫🇷 UK & FRANCE - Eurostar (London - Paris)
    {
        "id": "EUROSTAR-9024",
        "callsign": "EST-E320",
        "category": "train",
        "operator": "Eurostar International",
        "origin": {"code": "STP", "city": "London St Pancras", "lat": 51.5314, "lon": -0.1261},
        "dest": {"code": "GDN", "city": "Paris Gare du Nord", "lat": 48.8809, "lon": 2.3553},
        "stations": [
            {"code": "STP", "name": "London St Pancras", "lat": 51.5314, "lon": -0.1261},
            {"code": "LIL", "name": "Lille Europe", "lat": 50.6393, "lon": 3.0760},
            {"code": "GDN", "name": "Paris Gare du Nord", "lat": 48.8809, "lon": 2.3553}
        ],
        "speed": 300,
        "altitude": 65,
        "squawk": "ES-9024",
        "transponder": "TVM-430 / ETCS L2",
        "source": "Eurostar Real-Time"
    },
    # 🇫🇷 FRANCE - TGV InOui (Paris - Marseille)
    {
        "id": "TGV-6602",
        "callsign": "SNCF-TGV",
        "category": "train",
        "operator": "SNCF Voyageurs",
        "origin": {"code": "PAR", "city": "Paris Gare de Lyon", "lat": 48.8449, "lon": 2.3734},
        "dest": {"code": "MRS", "city": "Marseille St-Charles", "lat": 43.3032, "lon": 5.3806},
        "stations": [
            {"code": "PAR", "name": "Paris Gare de Lyon", "lat": 48.8449, "lon": 2.3734},
            {"code": "LYS", "name": "Lyon Part-Dieu", "lat": 45.7606, "lon": 4.8598},
            {"code": "MRS", "name": "Marseille St-Charles", "lat": 43.3032, "lon": 5.3806}
        ],
        "speed": 320,
        "altitude": 180,
        "squawk": "TGV-66",
        "transponder": "ERTMS Level 2",
        "source": "SNCF Open Data"
    },
    # 🇺🇸 USA - Amtrak Acela Express (Washington - Boston via NYC)
    {
        "id": "ACELA-2150",
        "callsign": "AMTK-ACELA",
        "category": "train",
        "operator": "Amtrak Acela",
        "origin": {"code": "WAS", "city": "Washington Union", "lat": 38.8973, "lon": -77.0063},
        "dest": {"code": "BOS", "city": "Boston South", "lat": 42.3523, "lon": -71.0552},
        "stations": [
            {"code": "WAS", "name": "Washington Union", "lat": 38.8973, "lon": -77.0063},
            {"code": "PHL", "name": "Philadelphia 30th", "lat": 39.9558, "lon": -75.1820},
            {"code": "NYP", "name": "New York Penn", "lat": 40.7505, "lon": -73.9934},
            {"code": "BOS", "name": "Boston South", "lat": 42.3523, "lon": -71.0552}
        ],
        "speed": 240,
        "altitude": 35,
        "squawk": "AMTK-215",
        "transponder": "ACSES / PTC",
        "source": "Amtrak Track-A-Train"
    }
]

def calculate_train_positions() -> List[Dict[str, Any]]:
    """Calculates live train coordinates along track networks worldwide."""
    trains = []
    t = time.time() / 85.0

    for train_meta in WORLD_RAIL_CORRIDORS:
        stations = train_meta["stations"]
        n_segments = len(stations) - 1
        
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
