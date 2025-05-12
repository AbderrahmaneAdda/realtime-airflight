BROKER_URL = 'localhost:9092'
TOPIC_NAME = 'flights-raw'  # topic Kafka
OPEN_SKY_URL = 'https://opensky-network.org/api/states/all'  # URL API OpenSky

# Configuration pour le producteur Kafka
KAFKA_PRODUCER_CONFIG = {
    'bootstrap_servers': [BROKER_URL],
    'request_timeout_ms': 60000,  # 60 s
    'metadata_max_age_ms': 300000,  # 5 min
    'retries': 5,
    'acks': 'all',  # Attente de la confirmation de tous les réplicas
}

FRANCE_BOUNDS = {
    'min_lat': 41.0,
    'max_lat': 51.5,
    'min_lon': -5.0,
    'max_lon': 9.5
}