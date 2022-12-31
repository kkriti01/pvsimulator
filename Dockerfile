#FROM python:3.7-alpine
FROM ubuntu:20.04
ENV PYTHONUNBUFFERED 1


RUN apt-get update -y \
    && apt-get install -y python3-pip python3-dev

COPY requirements.txt ./

RUN pip3 install --upgrade pip==20.0.1

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /

COPY . .

EXPOSE 15671 15672 7005


RUN chmod +x start.sh

CMD ["/start.sh"]