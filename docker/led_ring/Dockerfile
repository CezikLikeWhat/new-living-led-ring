FROM cezarymackowski/new-living-device-base:latest

ENV SERVER_ADDRESS=127.0.0.1 \
    RABBIT_LOGIN=device \
    RABBIT_PASSWORD=device \
    RABBIT_VHOST=new_living_vhost \
    LED_BRIGHTNESS=0.2

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py