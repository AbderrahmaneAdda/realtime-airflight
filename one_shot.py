import requests

# Bornes géographiques approximatives de la France
FRANCE_BOUNDS = {
    "min_lat": 41.0,
    "max_lat": 51.5,
    "min_lon": -5.0,
    "max_lon": 9.5
}

def is_in_france(lat, lon):
    return (
        FRANCE_BOUNDS["min_lat"] <= lat <= FRANCE_BOUNDS["max_lat"] and
        FRANCE_BOUNDS["min_lon"] <= lon <= FRANCE_BOUNDS["max_lon"]
    )

def fetch_flights_in_france():
    url = "https://opensky-network.org/api/states/all"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        states = data.get("states", [])

        flights_in_france = [
            s for s in states if s[6] is not None and s[5] is not None and is_in_france(s[6], s[5])
        ]

        print(f"Nombre de vols en cours au-dessus de la France : {len(flights_in_france)}")
    except requests.RequestException as e:
        print(f"Erreur lors de l'appel à l'API : {e}")

fetch_flights_in_france()
