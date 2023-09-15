import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, errors
from fastapi import FastAPI
from pydantic import BaseModel, StrictStr
from os import environ as env



app = FastAPI()

KAFKA_INSTANCE = env.get("KAFKA_INSTANCE","localhost:9092")

loop = asyncio.get_event_loop()

topic = env.get("topic")

consumer = AIOKafkaConsumer(topic, bootstrap_servers=KAFKA_INSTANCE, loop=loop)

async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
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


@app.on_event("startup")
async def startup_event():
    try:
        loop.create_task(consume())
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during startup: {kafka_error}")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        await consumer.stop()
    except errors.KafkaError as kafka_error:
        logging.error(f"Kafka error during shutdown: {kafka_error}")

@app.get("/consumer")
def read_root():
    return {f"Consuming {topic} sucessfully..check log for details"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
