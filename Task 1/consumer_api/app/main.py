import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, errors
from fastapi import FastAPI
from pydantic import BaseModel, StrictStr
from os import environ as env

# Create a FastAPI app instance
app = FastAPI()

# Get the Kafka instance address from environment variables or use a default value
KAFKA_INSTANCE = env.get("KAFKA_INSTANCE", "localhost:9092")

# Get the topic name from environment variables
topic = env.get("topic")

# Get the asyncio event loop
loop = asyncio.get_event_loop()

# Create an AIOKafkaConsumer instance for consuming messages from the specified topic
consumer = AIOKafkaConsumer(topic, bootstrap_servers=KAFKA_INSTANCE, loop=loop)

# Define an asynchronous function to consume messages from Kafka
async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            # Process the consumed message
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error while consuming: {kafka_error}")
    finally:
        await consumer.stop()

# Define an event handler to start message consumption when the app starts
@app.on_event("startup")
async def startup_event():
    try:
        # Create a task to run the consume function asynchronously
        loop.create_task(consume())
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during startup: {kafka_error}")

# Define an event handler to stop the Kafka consumer when the app shuts down
@app.on_event("shutdown")
async def shutdown_event():
    try:
        await consumer.stop()
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during shutdown: {kafka_error}")

# Define a root endpoint for the FastAPI app
@app.get("/consumer")
def read_root():
    return {f"Consuming {topic} successfully. Check the log for details."}

# Entry point for running the application
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
