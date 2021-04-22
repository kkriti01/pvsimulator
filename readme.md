This project includes 2 service:
 1. meter_reading.py which will generate random number in every 60 second and publish it to broker queue
 2. pvc_simulator.py reads that meter reading run some pv simulation and writes all the reading in a file.

This project also show a chart of power reading in every hour which is served by flask app and can be accessible on:
#### localhost:5000 

# Setup

## Install rabbitmq and setup Vhost using below link:
    I have used Vhost name as "PVSimulator"
    https://computingforgeeks.com/how-to-install-latest-rabbitmq-server-on-ubuntu-linux/

## Setup rabbit MQ:
     docker-compose -f docker-compose.yml up -d
## For starting and stopping the service below command will be used
    docker-compose -f docker-compose.yml start
    docker-compose -f .\docker-compose-tg.yml stop
    
## Build docker image:
    docker-compose -f docker-compose.yml up -d

## Run docker image:
    docker run pvsimulator_web
    flask server should be accessible on localhost:5000 
 