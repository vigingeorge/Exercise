import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer, errors
from fastapi import FastAPI
from pydantic import BaseModel, StrictStr
from os import environ as env

# Define a data model for the incoming message
class ProducerMessage(BaseModel):
    message: StrictStr = ""

# Create a FastAPI app instance
app = FastAPI()

# Get the Kafka instance address from environment variables or use a default value
KAFKA_INSTANCE = env.get("KAFKA_INSTANCE", "localhost:9092")

# Get the asyncio event loop
loop = asyncio.get_event_loop()

# Create an AIOKafkaProducer instance for producing messages
aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_INSTANCE)

# Define an event handler to start the Kafka producer when the app starts
@app.on_event("startup")
async def startup_event():
    try:
        await aioproducer.start()
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during startup: {kafka_error}")

# Define an event handler to stop the Kafka producer when the app shuts down
@app.on_event("shutdown")
async def shutdown_event():
    try:
        await aioproducer.stop()
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during shutdown: {kafka_error}")

# Define a root endpoint for the FastAPI app
@app.get("/")
def read_root():
    return {"Producer home"}

# Define an endpoint for producing messages to a Kafka topic
@app.post("/producer/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):
    try:
        # Produce the message to the specified Kafka topic
        await aioproducer.send(topicname, json.dumps(msg.dict()).encode("ascii"))
        response = {f"{msg} posted successfully on topic {topicname}"}
        return response
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error while producing: {kafka_error}")
        return {"error": "Failed to produce message to Kafka"}

# Entry point for running the application
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
