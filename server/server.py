#!/usr/bin/env python3

from asyncio.events import get_event_loop
from asyncio.futures import Future
from functools import partial
import asyncio
import json
import threading
import websockets

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

try:
    from secrets import secrets
except ImportError:
    print("Configuration secrets are kept in secrets.py, please add them there!")
    raise

def run_consumer(shutdown_flag, clients, lock):
    print("Starting Kafka Consumer.")
    schema_registry_client = SchemaRegistryClient(secrets["schema_registry"])
    deserializer = AvroDeserializer(schema_registry_client)
    config = secrets["consumer"] | {
        "group.id": "dashboard-demo",
        "value.deserializer": deserializer,
    }

    consumer = DeserializingConsumer(config)
    consumer.subscribe(["dashboard"])

    while not shutdown_flag.done():
        msg = consumer.poll(0.2)

        if msg is None:
            print("Waiting...")
        elif msg.error():
            print(f"ERROR: {msg.error()}")
        else:
            value = msg.value()
            formatted = json.dumps(value)
            print(f"Sending {formatted} to {clients}")

            with lock:
                websockets.broadcast(clients, formatted)

    print("Closing Kafka Consumer")
    consumer.close()


async def handle_connection(clients, lock, connection, path):
    with lock:
        clients.add(connection)

    await connection.wait_closed()

    with lock:
        clients.remove(connection)


async def main():
    shutdown_flag = Future()
    clients = set()
    lock = threading.Lock()

    get_event_loop().run_in_executor(None, run_consumer, shutdown_flag,
                                     clients, lock)

    print("Starting WebSocket Server.")
    try:
        async with websockets.serve(partial(handle_connection, clients, lock),
                                    None, 8080):
            await Future()
    finally:
        shutdown_flag.set_result(True)


asyncio.run(main())
