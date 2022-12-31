# PV Simulator

## running using docker-compose
1. `docker-compose up`
1. You'll see `meter` and `pv_simulator` service failing and restarting, this is fine, they are waiting for `rabbitmq` .
Once `rabbitmq` is up, they'll start normally
1. see logs in local `/logs` directory (host log is mapped to container)
1. see graph plot by opening 'http://127.0.0.1:7005' on your local machine

if port `7005` , `5672` and `15672` are busy on the host, please either free them or change port 
mapping in the `docker-compose.yml` file


## running manually
1. create virtual environment (python >= 3.7)
1. install dependencies: `pip install -r requirements.txt`
1. make sure rabbitmq is running
1. update rabbitmq connection url by exporting it to environment variable `RABBIT_MQ_HOST` or 
    directly updating in `settings.py` file
1. start meter : `python3 -m simulator.services.meter`
1. start pv_simulator : `python3 -m simulator.services.pv_simulator`
1. start web : `python3 -m simulator.services.web`
5. other variable can be controlled by os environment variable provided in settings.py


## The solution
1. meter.py: It simulates power consumption in home and generates random but continuous power and
   publish it to the broker.
2. simulator.py: Reads message from broker and generates simulated power value, adds that simulated value in power 
    meter reading and write it to the file.
3. web.py: It shows a plot which plots power meter reading(KW) with time.

 ## Improvement:
 1. More test cases can be added.
 2. Power value plot can be improved further. Also currently plot shows data for current date, one parameter can be added to select date and show reading for that date.