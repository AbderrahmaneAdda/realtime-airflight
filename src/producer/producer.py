from kafka import KafkaProducer
from dotenv import load_dotenv
from src.config import BROKER_URL, TOPIC_NAME, OPEN_SKY_URL, FRANCE_BOUNDS
import requests
import json
import time
import logging
import os

logging.basicConfig(level=logging.INFO)


def is_in_france(lat, lon):
    return (
        FRANCE_BOUNDS['min_lat'] <= lat <= FRANCE_BOUNDS['max_lat']
        and FRANCE_BOUNDS['min_lon'] <= lon <= FRANCE_BOUNDS['max_lon']
    )

def fetch_flight_data():
    try:
        response = requests.get(OPEN_SKY_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        states = data.get("states", [])
        filtered = []

        for state in states:
            if state[5] is not None and state[6] is not None: 
                lat = state[6] #lat
                lon = state[5] #long
                if is_in_france(lat, lon):
                    filtered.append({
                        "icao24": state[0],
                        "callsign": state[1],
                        "origin_country": state[2],
                        "time_position": state[3],
                        "last_contact": state[4],
                        "longitude": lon,
                        "latitude": lat,
                        "on_ground": state[8],
                        "velocity": state[9],
                        "vertical_rate": state[11],
                        "geo_altitude": state[13],
                    })
        return filtered
    except Exception as e:
        logging.error(f"Erreur lors de l'appel à l'API OpenSky: {e}")
        return []

def main():
    producer = KafkaProducer(
        bootstrap_servers=BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logging.info("Producteur Kafka initialisé")

    while True:
        flights = fetch_flight_data()
        for flight in flights:
            producer.send(TOPIC_NAME, flight)
            logging.info(f"Données envoyées: {flight.get('icao24')}")
        time.sleep(60)  # ne pas surcharger l’API

if __name__ == "__main__":
    main()
