import json
import logging
from confluent_kafka import Consumer, KafkaError, KafkaException
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Consumes login_success messages from Kafka topic."

    def handle(self, *args, **options):
        # Initialize Consumer using settings
        conf = settings.KAFKA_CONFIG
        consumer = Consumer(conf)
        
        topic_name = 'login_success'
        consumer.subscribe([topic_name])
        self.stdout.write(self.style.SUCCESS(f"Subscribed to topic '{topic_name}'..."))

        try:
            while True:
                # Poll for messages (timeout in seconds)
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition reached
                        continue
                    else:
                        raise KafkaException(msg.error())

                # Process message
                try:
                    payload = json.loads(msg.value().decode('utf-8'))
                    self.process_login_success(payload)
                except json.JSONDecodeError:
                    self.stderr.write(f"Failed to decode message: {msg.value()}")

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Stopping consumer loop..."))
        finally:
            # Cleanly leave consumer group and commit offsets
            consumer.close()

    def process_login_success(self, data):
        """
        Handle your business logic here (e.g., update Django models, log activity).
        """
        user_id = data.get('userId')
        username = data.get('username')
        email = data.get('email')

        self.stdout.write(self.style.SUCCESS(f"Login success for user: {username} (ID: {user_id}, Email: {email})"))