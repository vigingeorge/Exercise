import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer, errors
from fastapi import FastAPI
from pydantic import BaseModel, StrictStr
from os import environ as env


class ProducerMessage(BaseModel):
    message: StrictStr = ""


app = FastAPI()

KAFKA_INSTANCE = env.get("KAFKA_INSTANCE", "localhost:9092")

loop = asyncio.get_event_loop()

aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_INSTANCE)


@app.on_event("startup")
async def startup_event():
    try:
        await aioproducer.start()
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during startup: {kafka_error}")


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await aioproducer.stop()
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during shutdown: {kafka_error}")


@app.get("/")
def read_root():
    return {"Producer home"}


@app.post("/producer/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):
    try:
        await aioproducer.send(topicname, json.dumps(msg.dict()).encode("ascii"))
        response = {f"{msg} posted successfully on topic {topicname}"}
        return response
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error while producing: {kafka_error}")
        return {"error": "Failed to produce message to Kafka"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
