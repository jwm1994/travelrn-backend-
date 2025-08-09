from typing import Optional, Tuple

# Minimal centroids for testing. Extend with a full US city database in production.
CITY_STATE_CENTROIDS = {
    ("Austin","TX"): (30.2672, -97.7431),
    ("Houston","TX"): (29.7604, -95.3698),
    ("Dallas","TX"): (32.7767, -96.7970),
    ("San Antonio","TX"): (29.4241, -98.4936),
    ("Phoenix","AZ"): (33.4484, -112.0740),
    ("Denver","CO"): (39.7392, -104.9903),
    ("Miami","FL"): (25.7617, -80.1918),
    ("Atlanta","GA"): (33.7490, -84.3880),
    ("Chicago","IL"): (41.8781, -87.6298),
    ("Indianapolis","IN"): (39.7684, -86.1581),
    ("Detroit","MI"): (42.3314, -83.0458),
    ("Minneapolis","MN"): (44.9778, -93.2650),
    ("St. Louis","MO"): (38.6270, -90.1994),
    ("Charlotte","NC"): (35.2271, -80.8431),
    ("Omaha","NE"): (41.2565, -95.9345),
    ("Las Vegas","NV"): (36.1699, -115.1398),
    ("New York","NY"): (40.7128, -74.0060),
    ("Columbus","OH"): (39.9612, -82.9988),
    ("Portland","OR"): (45.5152, -122.6784),
    ("Philadelphia","PA"): (39.9526, -75.1652),
    ("Nashville","TN"): (36.1627, -86.7816),
    ("Dallas","TX"): (32.7767, -96.7970),
    ("Seattle","WA"): (47.6062, -122.3321),
}

def centroid(city: str, state: str) -> Optional[Tuple[float, float]]:
    key = (city.strip().title(), state.strip().upper())
    return CITY_STATE_CENTROIDS.get(key)
