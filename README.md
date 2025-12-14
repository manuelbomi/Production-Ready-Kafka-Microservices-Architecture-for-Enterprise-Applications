# Production-Ready Kafka Microservices Architecture for Enterprise Applications

##### A production-grade, Dockerized Apache Kafka platform demonstrating event-driven microservices architecture for enterprise and commerce applications.

##### This project showcases how to design, deploy, and scale Kafka-based systems using multiple domains, multiple consumer groups, and modern KRaft mode (no ZooKeeper).

---

## Project Overview

##### This repository demonstrates a realistic enterprise Kafka architecture where:

- One producer publishes events to multiple business domains

- Each domain is handled by its own microservice

- Each microservice has its own consumer group

- Kafka runs in KRaft mode with a multi-broker cluster

- The entire platform is Dockerized and production-aware

##### The system models a typical commerce / business workflow:

- Orders are created

- Payments are processed

- Shipments are dispatched

##### Each step is handled asynchronously using Kafka topics.

---

## Core Enterprise Principle

##### Each downstream service gets its own consumer group.

##### This ensures:

- [x] Independent scaling

- [x] Fault isolation

- [x] Clean separation of responsibilities

- [x] True microservices behavior

---

## Project Structure

```python
enterprise-kafka-platform/
│
├── docker-compose.yaml
│
├── producers/
│   └── producer.py
│
├── consumers/
│   ├── consumer_orders.py
│   ├── consumer_payments.py
│   └── consumer_shipping.py
│
├── .venv/
│
└── README.md

```
This structure is intentionally PyCharm-friendly and easy to scaffold for new services.

---

## Kafka Architecture – Topics & Consumers


#### Kafka Topic-Consumer Mapping

| Domain | Topic | Consumer App | Consumer Group | Function | Expected Load |
|--------|-------|--------------|----------------|----------|---------------|
| Order Management | `orders` | `consumer_orders.py` | `orders-service` | Processes order creation/updates | High |
| Payment Processing | `payments` | `consumer_payments.py` | `payments-service` | Handles payment transactions | Medium |
| Logistics | `shipping` | `consumer_shipping.py` | `shipping-service` | Manages shipping logistics | Medium |

### Design Notes:
- Each consumer group allows independent scaling per service
- Domain-driven topic naming for clarity
- Single responsibility consumers for maintainability
