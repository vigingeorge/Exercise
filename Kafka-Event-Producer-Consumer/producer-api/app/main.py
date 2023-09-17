"""Module providing a functionality of producing messages to kafka topic"""
import asyncio
import json
import logging

from os import environ as env
from aiokafka import AIOKafkaProducer, errors
from fastapi import FastAPI
from pydantic import BaseModel, StrictStr


class ProducerMessage(BaseModel):
    """ Define a data model for the incoming message"""
    message: StrictStr = ""


# Create a FastAPI app instance
app = FastAPI()

# Get the Kafka instance address from environment variables or use a default value
KAFKA_INSTANCE = env.get("KAFKA_INSTANCE", "localhost:9092")

# Get the asyncio event loop
loop = asyncio.get_event_loop()

# Create an AIOKafkaProducer instance for producing messages
aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_INSTANCE)


@app.on_event("startup")
async def startup_event():
    """ Define an event handler to start the Kafka producer when the app starts"""
    try:
        await aioproducer.start()
    except errors.KafkaError as kafka_error:
        logging.error("Kafka error during startup: %s", kafka_error)


@app.on_event("shutdown")
async def shutdown_event():
    """ Define an event handler to stop the Kafka producer when the app shuts down"""
    try:
        await aioproducer.stop()
    except errors.KafkaError as kafka_error:
        logging.error("Kafka error during shutdown: %s", kafka_error)


@app.get("/")
async def read_root():
    """ Define a root endpoint for the FastAPI app"""
    return {"Producer home"}


@app.post("/producer/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):
    """ Define an endpoint for producing messages to a Kafka topic"""
    try:
        # Produce the message to the specified Kafka topic
        await aioproducer.send(topicname, json.dumps(msg.dict()).encode("ascii"))
        response = {f"{msg} posted successfully on topic {topicname}"}
        return response
    except errors.KafkaError as kafka_error:
        logging.error("Kafka error while producing: %s", kafka_error)
        return {"error": "Failed to produce message to Kafka"}

# Entry point for running the application
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
