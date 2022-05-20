FROM alpine:3.15

RUN apk add --no-cache gcc musl-dev
RUN apk add --no-cache python3 python3-dev py3-pip
RUN apk add --no-cache librdkafka-dev

RUN pip install wheel
RUN pip install websockets 
RUN pip install confluent_kafka fastavro

RUN adduser -D webserver
USER webserver
WORKDIR /home/webserver

EXPOSE 8080

ADD server.py server.py
ADD secrets.py secrets.py

ENTRYPOINT ./server.py
