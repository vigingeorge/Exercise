# App development
## Create virtual enviroment
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


## Build consumer image
docker build -t producer-app .

## Create a topic 'test1'
docker exec kafka kafka-topics --create --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1 --topic test1

## Run the contaimer
docker run --network task1_broker-kafka -d -p 8000:8000 --name producer-container producer-app


## Test the endpoint for topic test1

 http://localhost:8000/producer/test1

Body example:

{"message":"me2"}

Result sample:

[
    "message='me2' posted successfully"
]

