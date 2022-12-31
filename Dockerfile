FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --upgrade bash

COPY requirements.txt ./

RUN pip3 install --upgrade pip==20.0.1

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /

EXPOSE 7005

COPY . .

RUN chmod +x start.sh

CMD ["/start.sh"]
