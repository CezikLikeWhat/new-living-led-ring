FROM python:3.10-alpine as new-living-device-base

WORKDIR /new-living/

COPY requirements.txt /new-living/requirements.txt

RUN apk add gcc \
            musl-dev \
            libc-dev && \
    pip3 install -r requirements.txt