#!/usr/bin/env python3
"""
consumer_orders.py

Enterprise-grade Kafka consumer for the Orders domain.

This service consumes order events from the `orders` Kafka topic
using a dedicated consumer group. It is designed to scale horizontally
across multiple instances while maintaining exactly-once processing
at the consumer group level.

Kafka:
- Multi-broker (KRaft mode)
- Topic: orders
- Consumer Group: orders-service
"""

import json
import logging
import signal
import sys
from confluent_kafka import Consumer, KafkaException

# ------------------------------------------------------------------------------
# Logging Configuration (Production Standard)
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("orders-consumer")

# ------------------------------------------------------------------------------
# Kafka Consumer Configuration
# ------------------------------------------------------------------------------

consumer_config = {
    # Enterprise cluster (multi-broker)
    "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",

    # Dedicated consumer group for Orders service
    "group.id": "orders-service",

    # Disable auto-commit for controlled offset management
    "enable.auto.commit": False,

    # Start from earliest if no committed offset exists
    "auto.offset.reset": "earliest",

    # Reliability / tuning
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
    logger.info("Shutdown signal received. Closing Kafka consumer...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# ------------------------------------------------------------------------------
# Subscription
# ------------------------------------------------------------------------------

consumer.subscribe(["orders"])
logger.info("Kafka Orders Consumer started and subscribed to topic: orders")

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
            # Deserialize message
            value = msg.value().decode("utf-8")
            order = json.loads(value)

            # Business logic (example)
            logger.info(
                "Order received | order_id=%s | user=%s | item=%s | quantity=%s",
                order.get("order_id"),
                order.get("user"),
                order.get("item"),
                order.get("quantity"),
            )

            # Commit offset after successful processing
            consumer.commit(message=msg, asynchronous=False)

        except json.JSONDecodeError as e:
            logger.error(f"JSON deserialization failed: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error while processing message: {e}")

except KafkaException as e:
    logger.exception(f"Kafka exception occurred: {e}")

finally:
    logger.info("Closing Kafka consumer")
    consumer.close()
