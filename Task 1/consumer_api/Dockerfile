FROM python:3.10-slim

# set work directory
WORKDIR /app

ENV KAFKA_INSTANCE 'kafka:29092'
ENV topic 'test1'

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./app  /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]