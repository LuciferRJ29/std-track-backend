import math
import time
from typing import List, Dict, Any

# Complete network of Indian Railways express trains & iconic world high-speed rail
WORLD_RAIL_CORRIDORS = [
    # 🇮🇳 INDIA - Vande Bharat Expresses (CRIS / RTIS)
    {
        "id": "VB-22436", "callsign": "VANDE-BHARAT-22436", "category": "train", "operator": "Indian Railways (NR)",
        "origin": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "dest": {"code": "BSB", "city": "Varanasi Jn", "lat": 25.3283, "lon": 82.9739},
        "stations": [
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188},
            {"code": "CNB", "name": "Kanpur Central", "lat": 26.4547, "lon": 80.3537},
            {"code": "PRYJ", "name": "Prayagraj Jn", "lat": 25.4526, "lon": 81.8349},
            {"code": "BSB", "name": "Varanasi Jn", "lat": 25.3283, "lon": 82.9739}
        ],
        "speed": 130, "altitude": 125, "squawk": "VB-22436", "transponder": "RTIS ISRO Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-20901", "callsign": "VANDE-BHARAT-20901", "category": "train", "operator": "Western Railway (WR)",
        "origin": {"code": "MMCT", "city": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        "dest": {"code": "ADI", "city": "Ahmedabad Jn", "lat": 23.0225, "lon": 72.5714},
        "stations": [
            {"code": "MMCT", "name": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
            {"code": "ST", "name": "Surat", "lat": 21.2049, "lon": 72.8411},
            {"code": "BRC", "name": "Vadodara Jn", "lat": 22.3107, "lon": 73.1812},
            {"code": "ADI", "name": "Ahmedabad Jn", "lat": 23.0225, "lon": 72.5714}
        ],
        "speed": 135, "altitude": 55, "squawk": "VB-20901", "transponder": "RTIS ISRO Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-20643", "callsign": "VANDE-BHARAT-20643", "category": "train", "operator": "Southern Railway (SR)",
        "origin": {"code": "MAS", "city": "Chennai Central", "lat": 13.0827, "lon": 80.2707},
        "dest": {"code": "CBE", "city": "Coimbatore Jn", "lat": 11.0168, "lon": 76.9558},
        "stations": [
            {"code": "MAS", "name": "Chennai Central", "lat": 13.0827, "lon": 80.2707},
            {"code": "SA", "name": "Salem Jn", "lat": 11.6643, "lon": 78.1460},
            {"code": "ED", "name": "Erode Jn", "lat": 11.3410, "lon": 77.7172},
            {"code": "CBE", "name": "Coimbatore Jn", "lat": 11.0168, "lon": 76.9558}
        ],
        "speed": 130, "altitude": 190, "squawk": "VB-20643", "transponder": "RTIS Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-20703", "callsign": "VANDE-BHARAT-20703", "category": "train", "operator": "South Central Railway (SCR)",
        "origin": {"code": "KCG", "city": "Hyderabad Kacheguda", "lat": 17.3916, "lon": 78.5020},
        "dest": {"code": "YPR", "city": "Bengaluru Yesvantpur", "lat": 13.0238, "lon": 77.5503},
        "stations": [
            {"code": "KCG", "name": "Hyderabad Kacheguda", "lat": 17.3916, "lon": 78.5020},
            {"code": "KRNT", "name": "Kurnool City", "lat": 15.8281, "lon": 78.0373},
            {"code": "ATP", "name": "Anantapur", "lat": 14.6819, "lon": 77.6006},
            {"code": "YPR", "name": "Bengaluru Yesvantpur", "lat": 13.0238, "lon": 77.5503}
        ],
        "speed": 125, "altitude": 510, "squawk": "VB-20703", "transponder": "RTIS Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-22457", "callsign": "VANDE-BHARAT-22457", "category": "train", "operator": "Northern Railway (NR)",
        "origin": {"code": "ANVT", "city": "Anand Vihar Delhi", "lat": 28.6506, "lon": 77.3152},
        "dest": {"code": "DDN", "city": "Dehradun", "lat": 30.3155, "lon": 78.0322},
        "stations": [
            {"code": "ANVT", "name": "Anand Vihar", "lat": 28.6506, "lon": 77.3152},
            {"code": "MTC", "name": "Meerut City", "lat": 28.9800, "lon": 77.6900},
            {"code": "RK", "name": "Roorkee", "lat": 29.8660, "lon": 77.8940},
            {"code": "HW", "name": "Haridwar", "lat": 29.9560, "lon": 78.1630},
            {"code": "DDN", "name": "Dehradun", "lat": 30.3155, "lon": 78.0322}
        ],
        "speed": 120, "altitude": 480, "squawk": "VB-22457", "transponder": "RTIS Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-20171", "callsign": "VANDE-BHARAT-20171", "category": "train", "operator": "West Central Railway (WCR)",
        "origin": {"code": "RKMP", "city": "Bhopal Rani Kamlapati", "lat": 23.2185, "lon": 77.4375},
        "dest": {"code": "NZM", "city": "Hazrat Nizamuddin Delhi", "lat": 28.5888, "lon": 77.2534},
        "stations": [
            {"code": "RKMP", "name": "Rani Kamlapati", "lat": 23.2185, "lon": 77.4375},
            {"code": "VGLJ", "name": "VGL Jhansi", "lat": 25.4484, "lon": 78.5685},
            {"code": "GWL", "name": "Gwalior", "lat": 26.2183, "lon": 78.1828},
            {"code": "AGC", "name": "Agra Cantt", "lat": 27.1593, "lon": 77.9942},
            {"code": "NZM", "name": "Hazrat Nizamuddin", "lat": 28.5888, "lon": 77.2534}
        ],
        "speed": 140, "altitude": 220, "squawk": "VB-20171", "transponder": "RTIS Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-22895", "callsign": "VANDE-BHARAT-22895", "category": "train", "operator": "South Eastern Railway (SER)",
        "origin": {"code": "HWH", "city": "Howrah Jn", "lat": 22.5839, "lon": 88.3426},
        "dest": {"code": "PURI", "city": "Puri", "lat": 19.8135, "lon": 85.8312},
        "stations": [
            {"code": "HWH", "name": "Howrah Jn", "lat": 22.5839, "lon": 88.3426},
            {"code": "KGP", "name": "Kharagpur Jn", "lat": 22.3300, "lon": 87.3200},
            {"code": "BBS", "name": "Bhubaneswar", "lat": 20.2667, "lon": 85.8436},
            {"code": "PURI", "name": "Puri", "lat": 19.8135, "lon": 85.8312}
        ],
        "speed": 130, "altitude": 45, "squawk": "VB-22895", "transponder": "RTIS Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-22225", "callsign": "VANDE-BHARAT-22225", "category": "train", "operator": "Central Railway (CR)",
        "origin": {"code": "CSMT", "city": "Mumbai CSMT", "lat": 18.9400, "lon": 72.8353},
        "dest": {"code": "SUR", "city": "Solapur Jn", "lat": 17.6599, "lon": 75.9064},
        "stations": [
            {"code": "CSMT", "name": "Mumbai CSMT", "lat": 18.9400, "lon": 72.8353},
            {"code": "KYN", "name": "Kalyan Jn", "lat": 19.2437, "lon": 73.1355},
            {"code": "PUNE", "name": "Pune Jn", "lat": 18.5289, "lon": 73.8744},
            {"code": "SUR", "name": "Solapur", "lat": 17.6599, "lon": 75.9064}
        ],
        "speed": 125, "altitude": 470, "squawk": "VB-22225", "transponder": "RTIS Satellite", "source": "CRIS Live Rail"
    },
    {
        "id": "VB-22229", "callsign": "VANDE-BHARAT-GOA", "category": "train", "operator": "Konkan Railway (KR)",
        "origin": {"code": "CSMT", "city": "Mumbai CSMT", "lat": 18.9400, "lon": 72.8353},
        "dest": {"code": "MAO", "city": "Madgaon Goa", "lat": 15.2736, "lon": 73.9581},
        "stations": [
            {"code": "CSMT", "name": "Mumbai CSMT", "lat": 18.9400, "lon": 72.8353},
            {"code": "PNVL", "name": "Panvel", "lat": 18.9900, "lon": 73.1200},
            {"code": "RN", "name": "Ratnagiri", "lat": 16.9800, "lon": 73.3200},
            {"code": "MAO", "name": "Madgaon Goa", "lat": 15.2736, "lon": 73.9581}
        ],
        "speed": 120, "altitude": 80, "squawk": "VB-22229", "transponder": "RTIS Satellite", "source": "Konkan Railway"
    },
    {
        "id": "VB-20633", "callsign": "VANDE-BHARAT-KERALA", "category": "train", "operator": "Southern Railway (SR)",
        "origin": {"code": "KGQ", "city": "Kasaragod", "lat": 12.5000, "lon": 74.9900},
        "dest": {"code": "TVC", "city": "Thiruvananthapuram Central", "lat": 8.4875, "lon": 76.9525},
        "stations": [
            {"code": "KGQ", "name": "Kasaragod", "lat": 12.5000, "lon": 74.9900},
            {"code": "CLT", "name": "Kozhikode", "lat": 11.2480, "lon": 75.7804},
            {"code": "ERS", "name": "Ernakulam Jn", "lat": 9.9675, "lon": 76.2917},
            {"code": "TVC", "name": "Thiruvananthapuram", "lat": 8.4875, "lon": 76.9525}
        ],
        "speed": 115, "altitude": 30, "squawk": "VB-20633", "transponder": "RTIS Satellite", "source": "CRIS Live Rail"
    },

    # 🇮🇳 INDIA - Rajdhani & Shatabdi Expresses
    {
        "id": "RAJ-12952", "callsign": "MUMBAI-RAJDHANI", "category": "train", "operator": "Western Railway (WR)",
        "origin": {"code": "MMCT", "city": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        "dest": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "stations": [
            {"code": "MMCT", "name": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
            {"code": "ST", "name": "Surat", "lat": 21.2049, "lon": 72.8411},
            {"code": "BRC", "name": "Vadodara Jn", "lat": 22.3107, "lon": 73.1812},
            {"code": "KOTA", "name": "Kota Jn", "lat": 25.2138, "lon": 75.8648},
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188}
        ],
        "speed": 130, "altitude": 210, "squawk": "RAJ-12952", "transponder": "RTIS Live", "source": "CRIS Track"
    },
    {
        "id": "RAJ-12302", "callsign": "HOWRAH-RAJDHANI", "category": "train", "operator": "Eastern Railway (ER)",
        "origin": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "dest": {"code": "HWH", "city": "Howrah Kolkata", "lat": 22.5839, "lon": 88.3426},
        "stations": [
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188},
            {"code": "CNB", "name": "Kanpur Central", "lat": 26.4547, "lon": 80.3537},
            {"code": "PRYJ", "name": "Prayagraj Jn", "lat": 25.4526, "lon": 81.8349},
            {"code": "DDU", "name": "Pt Deen Dayal Upadhyaya", "lat": 25.2800, "lon": 83.1100},
            {"code": "GAYA", "name": "Gaya Jn", "lat": 24.8000, "lon": 85.0000},
            {"code": "HWH", "name": "Howrah Jn", "lat": 22.5839, "lon": 88.3426}
        ],
        "speed": 130, "altitude": 110, "squawk": "RAJ-12302", "transponder": "RTIS Live", "source": "CRIS Track"
    },
    {
        "id": "RAJ-22692", "callsign": "BENGALURU-RAJDHANI", "category": "train", "operator": "South Western Railway (SWR)",
        "origin": {"code": "SBC", "city": "Bengaluru KSR", "lat": 12.9780, "lon": 77.5696},
        "dest": {"code": "NZM", "city": "Hazrat Nizamuddin Delhi", "lat": 28.5888, "lon": 77.2534},
        "stations": [
            {"code": "SBC", "name": "Bengaluru KSR", "lat": 12.9780, "lon": 77.5696},
            {"code": "SC", "name": "Secunderabad Jn", "lat": 17.4344, "lon": 78.5013},
            {"code": "NGP", "name": "Nagpur Jn", "lat": 21.1528, "lon": 79.0882},
            {"code": "BPL", "name": "Bhopal Jn", "lat": 23.2599, "lon": 77.4126},
            {"code": "NZM", "name": "Hazrat Nizamuddin", "lat": 28.5888, "lon": 77.2534}
        ],
        "speed": 125, "altitude": 620, "squawk": "RAJ-22692", "transponder": "RTIS Live", "source": "CRIS Track"
    },
    {
        "id": "SHAT-12002", "callsign": "BHOPAL-SHATABDI", "category": "train", "operator": "Northern Railway (NR)",
        "origin": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "dest": {"code": "RKMP", "city": "Bhopal Rani Kamlapati", "lat": 23.2185, "lon": 77.4375},
        "stations": [
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188},
            {"code": "AGC", "name": "Agra Cantt", "lat": 27.1593, "lon": 77.9942},
            {"code": "GWL", "name": "Gwalior", "lat": 26.2183, "lon": 78.1828},
            {"code": "VGLJ", "name": "VGL Jhansi", "lat": 25.4484, "lon": 78.5685},
            {"code": "RKMP", "name": "Rani Kamlapati", "lat": 23.2185, "lon": 77.4375}
        ],
        "speed": 140, "altitude": 190, "squawk": "SHAT-12002", "transponder": "RTIS Satellite", "source": "CRIS Track"
    },

    # 🇯🇵 JAPAN - Shinkansen Bullet Trains
    {
        "id": "SHIN-NOZOMI-01", "callsign": "SHINKANSEN-NOZOMI", "category": "train", "operator": "JR Central (Tokaido Line)",
        "origin": {"code": "TYO-STN", "city": "Tokyo Station", "lat": 35.6812, "lon": 139.7671},
        "dest": {"code": "OSA-STN", "city": "Shin-Osaka Station", "lat": 34.7335, "lon": 135.5003},
        "stations": [
            {"code": "TYO", "name": "Tokyo Station", "lat": 35.6812, "lon": 139.7671},
            {"code": "NAG", "name": "Nagoya Station", "lat": 35.1709, "lon": 136.8815},
            {"code": "KYO", "name": "Kyoto Station", "lat": 34.9858, "lon": 135.7588},
            {"code": "OSA", "name": "Shin-Osaka", "lat": 34.7335, "lon": 135.5003}
        ],
        "speed": 285, "altitude": 25, "squawk": "SHIN-NZ-01", "transponder": "ATC / Shinkansen RT", "source": "JR Central Live"
    },
    {
        "id": "SHIN-HAYABUSA-05", "callsign": "SHINKANSEN-HAYABUSA", "category": "train", "operator": "JR East (Tohoku Line)",
        "origin": {"code": "TYO-STN", "city": "Tokyo Station", "lat": 35.6812, "lon": 139.7671},
        "dest": {"code": "AOM-STN", "city": "Shin-Aomori Station", "lat": 40.8286, "lon": 140.6936},
        "stations": [
            {"code": "TYO", "name": "Tokyo Station", "lat": 35.6812, "lon": 139.7671},
            {"code": "SEN", "name": "Sendai Station", "lat": 38.2601, "lon": 140.8824},
            {"code": "MOR", "name": "Morioka Station", "lat": 39.7020, "lon": 141.1360},
            {"code": "AOM", "name": "Shin-Aomori", "lat": 40.8286, "lon": 140.6936}
        ],
        "speed": 320, "altitude": 45, "squawk": "SHIN-HB-05", "transponder": "DS-ATC", "source": "JR East Live"
    },

    # 🇪🇺 EUROPE - Eurostar & TGV & ICE & AVE
    {
        "id": "EUROSTAR-9014", "callsign": "EUROSTAR-9014", "category": "train", "operator": "Eurostar International",
        "origin": {"code": "STP", "city": "London St Pancras", "lat": 51.5314, "lon": -0.1261},
        "dest": {"code": "GDN", "city": "Paris Gare du Nord", "lat": 48.8809, "lon": 2.3553},
        "stations": [
            {"code": "STP", "name": "London St Pancras", "lat": 51.5314, "lon": -0.1261},
            {"code": "TUN", "name": "Channel Tunnel Transit", "lat": 51.0928, "lon": 1.2570},
            {"code": "LIL", "name": "Lille Europe", "lat": 50.6389, "lon": 3.0760},
            {"code": "GDN", "name": "Paris Gare du Nord", "lat": 48.8809, "lon": 2.3553}
        ],
        "speed": 300, "altitude": 40, "squawk": "EST-9014", "transponder": "ETCS Level 2", "source": "Eurostar Live"
    },
    {
        "id": "TGV-INQUI-6612", "callsign": "TGV-MEDITERRANEE", "category": "train", "operator": "SNCF Voyageurs",
        "origin": {"code": "PLY", "city": "Paris Gare de Lyon", "lat": 48.8443, "lon": 2.3744},
        "dest": {"code": "MSC", "city": "Marseille Saint-Charles", "lat": 43.3028, "lon": 5.3806},
        "stations": [
            {"code": "PLY", "name": "Paris Gare de Lyon", "lat": 48.8443, "lon": 2.3744},
            {"code": "LYN", "name": "Lyon Part-Dieu", "lat": 45.7606, "lon": 4.8594},
            {"code": "AVI", "name": "Avignon TGV", "lat": 43.9219, "lon": 4.7861},
            {"code": "MSC", "name": "Marseille Saint-Charles", "lat": 43.3028, "lon": 5.3806}
        ],
        "speed": 320, "altitude": 110, "squawk": "TGV-6612", "transponder": "TVM 430", "source": "SNCF Open Data"
    },
    {
        "id": "ICE-SPRINTER-704", "callsign": "ICE-SPRINTER", "category": "train", "operator": "Deutsche Bahn (DB)",
        "origin": {"code": "BLN", "city": "Berlin Hbf", "lat": 52.5251, "lon": 13.3694},
        "dest": {"code": "MUN", "city": "Munich Hbf", "lat": 48.1402, "lon": 11.5583},
        "stations": [
            {"code": "BLN", "name": "Berlin Hbf", "lat": 52.5251, "lon": 13.3694},
            {"code": "LEI", "name": "Leipzig Hbf", "lat": 51.3456, "lon": 12.3812},
            {"code": "NUE", "name": "Nuremberg Hbf", "lat": 49.4456, "lon": 11.0825},
            {"code": "MUN", "name": "Munich Hbf", "lat": 48.1402, "lon": 11.5583}
        ],
        "speed": 300, "altitude": 320, "squawk": "ICE-704", "transponder": "LZB / ETCS", "source": "DB Telematics"
    },
    {
        "id": "AVE-03102", "callsign": "AVE-MADRID-BARCELONA", "category": "train", "operator": "Renfe Operadora",
        "origin": {"code": "MAD", "city": "Madrid Puerta de Atocha", "lat": 40.4068, "lon": -3.6908},
        "dest": {"code": "BCN", "city": "Barcelona Sants", "lat": 41.3790, "lon": 2.1400},
        "stations": [
            {"code": "MAD", "name": "Madrid Atocha", "lat": 40.4068, "lon": -3.6908},
            {"code": "ZAZ", "name": "Zaragoza Delicias", "lat": 41.6586, "lon": -0.9125},
            {"code": "BCN", "name": "Barcelona Sants", "lat": 41.3790, "lon": 2.1400}
        ],
        "speed": 310, "altitude": 250, "squawk": "AVE-3102", "transponder": "ETCS Level 2", "source": "Renfe Live"
    },

    # 🇺🇸 USA - Amtrak High-Speed
    {
        "id": "ACELA-2150", "callsign": "AMTK-ACELA", "category": "train", "operator": "Amtrak Acela",
        "origin": {"code": "WAS", "city": "Washington Union", "lat": 38.8973, "lon": -77.0063},
        "dest": {"code": "BOS", "city": "Boston South", "lat": 42.3523, "lon": -71.0552},
        "stations": [
            {"code": "WAS", "name": "Washington Union", "lat": 38.8973, "lon": -77.0063},
            {"code": "PHL", "name": "Philadelphia 30th", "lat": 39.9558, "lon": -75.1820},
            {"code": "NYP", "name": "New York Penn", "lat": 40.7505, "lon": -73.9934},
            {"code": "BOS", "name": "Boston South", "lat": 42.3523, "lon": -71.0552}
        ],
        "speed": 240, "altitude": 35, "squawk": "AMTK-2150", "transponder": "ACSES / PTC", "source": "Amtrak Track-A-Train"
    },

    # 🇨🇳 CHINA - CR400 Fuxing High Speed Rail
    {
        "id": "CR400-G1", "callsign": "CR400-FUXING-BEIJING-SHANGHAI", "category": "train", "operator": "China Railway (CR)",
        "origin": {"code": "BJS", "city": "Beijing South", "lat": 39.8653, "lon": 116.3789},
        "dest": {"code": "SHA-HQ", "city": "Shanghai Hongqiao", "lat": 31.1947, "lon": 121.3200},
        "stations": [
            {"code": "BJS", "name": "Beijing South", "lat": 39.8653, "lon": 116.3789},
            {"code": "TJN", "name": "Tianjin West", "lat": 39.1550, "lon": 117.1620},
            {"code": "JIN", "name": "Jinan West", "lat": 36.6660, "lon": 116.8920},
            {"code": "NAN", "name": "Nanjing South", "lat": 31.9700, "lon": 118.7960},
            {"code": "SHA-HQ", "name": "Shanghai Hongqiao", "lat": 31.1947, "lon": 121.3200}
        ],
        "speed": 350, "altitude": 40, "squawk": "CR400-G1", "transponder": "CTCS-3", "source": "China Railway 12306"
    }
]

def calculate_train_positions() -> List[Dict[str, Any]]:
    """Calculates live train coordinates along track networks worldwide."""
    trains = []
    t = time.time() / 70.0

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
