from kafka import KafkaConsumer
import json
import logging
import time

logging.basicConfig(level=logging.INFO)

TOPIC_NAME = 'flights-raw'
BROKER_URL = 'localhost:9092'

# Dictionnaire pour stocker les vols
flights_in_air = {}

def main():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[BROKER_URL],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='flight-counter-group'
    )

    logging.info(f"[OK] Connecté au topic Kafka '{TOPIC_NAME}'. Début du comptage...")

    # Initialisation de last_print_time pour éviter l'erreur
    last_print_time = time.time()

    try:
        for message in consumer:
            flight = message.value
            icao24 = flight.get("icao24")

            # Vérifier si le vol est toujours en vol
            if flight.get("on_ground"):
                if icao24 in flights_in_air:
                    del flights_in_air[icao24]  # Supprimer le vol du dictionnaire si "on ground"
                    logging.info(f"Vol {icao24} atterri, supprimé du dictionnaire.")
            else:
                if icao24 not in flights_in_air:
                    flights_in_air[icao24] = flight  # Ajouter le vol au dictionnaire s'il n'y est pas déjà
                    logging.info(f"Vol {icao24} ajouté au dictionnaire.")

            # Afficher le nombre de vols en l'air toutes les 10 secondes
            current_time = time.time()
            if current_time - last_print_time >= 10:
                logging.info(f"Vols en l'air : {len(flights_in_air)}")
                last_print_time = current_time

    except KeyboardInterrupt:
        logging.info("Arrêt du consumer.")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
