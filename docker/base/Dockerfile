FROM python:3.10.9-slim-bullseye as new-living-device-base

WORKDIR /new-living/

COPY requirements.txt /new-living/requirements.txt

RUN apt update -y && \
    apt install -y gcc python3-rpi.gpio && \
    pip3 install -r requirements.txt
