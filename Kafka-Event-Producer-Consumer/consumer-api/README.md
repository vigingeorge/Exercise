## Create virtual enviroment
py -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt


## Build consumer image
docker build -t consumer-app .

## Run the container
docker run --network task1_broker-kafka -d -p 80:80 --name consumer-container consumer-app

## Test the endpoint for topic test1

http://localhost:80/consumer


Result sample:

[
    "Consuming test1 sucessfully..check log for details"
]

