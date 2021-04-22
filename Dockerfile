FROM ubuntu:20.04
MAINTAINER Kriti Kumari "kriti.cs10@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN python3 -m pip install --upgrade pip==20.3.4

RUN pip install -r requirements.txt

COPY . /

CMD [ "python", "./services/meter_reading.py" ]
CMD [ "python", "./mq/consume_messages.py" ]

ENV FLASK_APP="apis\pvsimulations_apis.py"
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
COPY . .
CMD ["flask", "run"]