# Simulated values for academic purposes — not real-world measurements.
# Source: Algorithm Design & Analysis course project, Tanta University.

NODES = [
    {"id": "haram",       "display_name": "Masjid Al Haram", "coordinates": (0,    0)},
    {"id": "mina",        "display_name": "Mina",            "coordinates": (5,    2.5)},
    {"id": "muzdalifah",  "display_name": "Muzdalifah",      "coordinates": (9,    1)},
    {"id": "arafat",      "display_name": "Arafat",          "coordinates": (13,   0)},
    {"id": "jamarat",     "display_name": "Jamarat",         "coordinates": (5.5,  4)},
]

EDGES = [
    {"source": "haram",      "target": "mina",       "distance_km": 8,    "capacity_per_hour": 80_000,  "current_load_percent": 65},
    {"source": "haram",      "target": "arafat",     "distance_km": 20,   "capacity_per_hour": 60_000,  "current_load_percent": 40},
    {"source": "mina",       "target": "muzdalifah", "distance_km": 4,    "capacity_per_hour": 100_000, "current_load_percent": 80},
    {"source": "mina",       "target": "jamarat",    "distance_km": 1.5,  "capacity_per_hour": 120_000, "current_load_percent": 90},
    {"source": "mina",       "target": "arafat",     "distance_km": 12,   "capacity_per_hour": 70_000,  "current_load_percent": 55},
    {"source": "muzdalifah", "target": "arafat",     "distance_km": 9,    "capacity_per_hour": 90_000,  "current_load_percent": 70},
    {"source": "muzdalifah", "target": "jamarat",    "distance_km": 5,    "capacity_per_hour": 85_000,  "current_load_percent": 60},
    {"source": "arafat",     "target": "jamarat",    "distance_km": 14,   "capacity_per_hour": 50_000,  "current_load_percent": 30},
    {"source": "haram",      "target": "jamarat",    "distance_km": 7,    "capacity_per_hour": 75_000,  "current_load_percent": 50},
    {"source": "haram",      "target": "muzdalifah", "distance_km": 11,   "capacity_per_hour": 65_000,  "current_load_percent": 45},
]
