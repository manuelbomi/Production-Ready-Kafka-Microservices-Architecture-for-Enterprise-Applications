import json
import uuid
from confluent_kafka import Producer

producer_config = {
    "bootstrap.servers": "localhost:9092,localhost:9093,localhost:9094",
    "acks": "all",
    "retries": 5,
}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(
            f"✅ Delivered to {msg.topic()} | "
            f"partition {msg.partition()} | "
            f"offset {msg.offset()}"
        )

def send_event(topic, payload):
    producer.produce(
        topic=topic,
        value=json.dumps(payload).encode("utf-8"),
        callback=delivery_report
    )
    producer.poll(0)

# Orders event
send_event("orders", {
    "order_id": str(uuid.uuid4()),
    "user": "Moses Thomas",
    "item": "Car",
    "quantity": 23
})

# Payments event
send_event("payments", {
    "payment_id": str(uuid.uuid4()),
    "order_amount": 40,
    "currency": "USD",
    "status": "PAID"
})

# Shipping event
send_event("shipping", {
    "shipment_id": str(uuid.uuid4()),
    "carrier": "FedEx",
    "status": "DISPATCHED"
})

producer.flush()
