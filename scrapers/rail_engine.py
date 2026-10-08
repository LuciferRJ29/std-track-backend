import math
import time
from typing import List, Dict, Any

# Real rail corridor coordinates with intermediate stops
RAIL_CORRIDORS = [
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
        "squawk": "VB-01",
        "transponder": "RTIS ISRO Satellite",
        "source": "CRIS / National Rail Portal"
    },
    {
        "id": "RAJ-12952",
        "callsign": "RAJDHANI-12952",
        "category": "train",
        "operator": "Western Railway",
        "origin": {"code": "MMCT", "city": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        "dest": {"code": "NDLS", "city": "New Delhi", "lat": 28.6424, "lon": 77.2188},
        "stations": [
            {"code": "MMCT", "name": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
            {"code": "ST", "name": "Surat", "lat": 21.2049, "lon": 72.8411},
            {"code": "BRC", "name": "Vadodara", "lat": 22.3107, "lon": 73.1812},
            {"code": "RTM", "name": "Ratlam", "lat": 23.3344, "lon": 75.0375},
            {"code": "KOTA", "name": "Kota Jn", "lat": 25.2138, "lon": 75.8648},
            {"code": "NDLS", "name": "New Delhi", "lat": 28.6424, "lon": 77.2188}
        ],
        "speed": 125,
        "altitude": 90,
        "squawk": "WR-12952",
        "transponder": "RTIS Telemetry",
        "source": "IRCTC / GTFS-RT"
    },
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
    {
        "id": "TGV-6602",
        "callsign": "SNCF-TGV",
        "category": "train",
        "operator": "SNCF France",
        "origin": {"code": "LYS", "city": "Lyon Part-Dieu", "lat": 45.7606, "lon": 4.8598},
        "dest": {"code": "PAR", "city": "Paris Gare de Lyon", "lat": 48.8449, "lon": 2.3734},
        "stations": [
            {"code": "LYS", "name": "Lyon Part-Dieu", "lat": 45.7606, "lon": 4.8598},
            {"code": "PAR", "name": "Paris Gare de Lyon", "lat": 48.8449, "lon": 2.3734}
        ],
        "speed": 310,
        "altitude": 210,
        "squawk": "TGV-66",
        "transponder": "ERTMS Level 2",
        "source": "SNCF Open Data"
    }
]

def calculate_train_positions() -> List[Dict[str, Any]]:
    """Calculates train coordinates along their track network based on elapsed time."""
    trains = []
    t = time.time() / 100.0  # Time factor for continuous cyclical progression

    for train_meta in RAIL_CORRIDORS:
        stations = train_meta["stations"]
        n_segments = len(stations) - 1
        
        # Smooth cyclical parameter between 0 and 1
        progress = (math.sin(t + hash(train_meta["id"]) % 10) + 1.0) / 2.0
        scaled = progress * n_segments
        seg_idx = min(int(scaled), n_segments - 1)
        seg_frac = scaled - seg_idx

        s1 = stations[seg_idx]
        s2 = stations[seg_idx + 1]

        # Interpolate coordinates along the track
        lat = s1["lat"] + (s2["lat"] - s1["lat"]) * seg_frac
        lon = s1["lon"] + (s2["lon"] - s1["lon"]) * seg_frac

        # Calculate track bearing / heading
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
            "status": f"Track Segment: {s1['name']} → {s2['name']}",
            "eta": "Running On Time",
            "fuel": 98,
            "squawk": train_meta["squawk"],
            "transponder": train_meta["transponder"],
            "source": train_meta["source"]
        })

    return trains
