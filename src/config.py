# src/config.py

BROKER_URL = 'localhost:9092'  # Utiliser localhost quand on est en dehors du réseau Docker
TOPIC_NAME = 'flights-raw'  # Nom du topic Kafka
OPEN_SKY_URL = 'https://opensky-network.org/api/states/all'  # URL de l'API OpenSky

# Configuration pour le producteur Kafka
KAFKA_PRODUCER_CONFIG = {
    'bootstrap_servers': [BROKER_URL],
    'request_timeout_ms': 60000,  # Timeout à 60 secondes
    'metadata_max_age_ms': 300000,  # Délai pour actualiser les métadonnées (5 minutes)
    'retries': 5,  # Tentatives en cas d'échec de connexion
    'acks': 'all',  # Attente de la confirmation de tous les réplicas
}

FRANCE_BOUNDS = {
    'min_lat': 41.0,
    'max_lat': 51.5,
    'min_lon': -5.0,
    'max_lon': 9.5
}