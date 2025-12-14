#!/usr/bin/env python3
"""
consumer_shipping.py

Enterprise-grade Kafka consumer for the Shipping domain.

This service consumes shipping events from the `shipping` Kafka topic
using a dedicated consumer group. It is responsible for logistics and
delivery state transitions.

Kafka:
- Multi-broker (KRaft mode)
- Topic: shipping
- Consumer Group: shipping-service
"""

import json
import logging
import signal
from confluent_kafka import Consumer, KafkaException

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("shipping-consumer")

# ------------------------------------------------------------------------------
# Kafka Consumer Configuration
# ------------------------------------------------------------------------------

consumer_config = {
    "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",
    "group.id": "shipping-service",
    "enable.auto.commit": False,
    "auto.offset.reset": "earliest",
    "session.timeout.ms": 10000,
    "max.poll.interval.ms": 300000,
}

consumer = Consumer(consumer_config)

# ------------------------------------------------------------------------------
# Graceful Shutdown Handling
# ------------------------------------------------------------------------------

running = True

def shutdown(signal_received, frame):
    global running
    logger.info("Shutdown signal received. Closing Shipping consumer...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# ------------------------------------------------------------------------------
# Subscription
# ------------------------------------------------------------------------------

consumer.subscribe(["shipping"])
logger.info("Kafka Shipping Consumer started and subscribed to topic: shipping")

# ------------------------------------------------------------------------------
# Message Processing Loop
# ------------------------------------------------------------------------------

try:
    while running:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(f"Kafka error: {msg.error()}")
            continue

        try:
            value = msg.value().decode("utf-8")
            shipment = json.loads(value)

            # Business logic (example)
            logger.info(
                "Shipment update | shipment_id=%s | carrier=%s | status=%s",
                shipment.get("shipment_id"),
                shipment.get("carrier"),
                shipment.get("status"),
            )

            # Commit offset after successful processing
            consumer.commit(message=msg, asynchronous=False)

        except json.JSONDecodeError as e:
            logger.error(f"JSON deserialization failed: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error while processing shipment: {e}")

except KafkaException as e:
    logger.exception(f"Kafka exception occurred: {e}")

finally:
    logger.info("Closing Shipping consumer")
    consumer.close()
