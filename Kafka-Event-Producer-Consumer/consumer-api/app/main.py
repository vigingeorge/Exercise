"""Module providing functionality of consuming messages from kafka topic."""
import asyncio
import logging

from os import environ as env
from aiokafka import AIOKafkaConsumer, errors
from fastapi import FastAPI

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


async def consume():
    """ Define an asynchronous function to consume messages from Kafka """
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
        logging.error("Kafka error while consuming: %s", kafka_error)
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    """ Define an event handler to start message consumption when the app starts"""
    try:
        # Create a task to run the consume function asynchronously
        loop.create_task(consume())
    except errors.KafkaError as kafka_error:
        logging.error("Kafka error during startup: %s", kafka_error)


@app.on_event("shutdown")
async def shutdown_event():
    """ Define an event handler to stop the Kafka consumer when the app shuts down"""
    try:
        await consumer.stop()
    except errors.KafkaError as kafka_error:
        logging.error("Kafka error during shutdown: %s", kafka_error)


@app.get("/consumer")
def read_root():
    """ Define a root endpoint for the FastAPI app """
    return {"Consuming %s successfully. Check the log for details."% topic}


# Entry point for running the application
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
