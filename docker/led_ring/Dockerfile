FROM new-living-device-base

ENV SERVER_ADDRES=127.0.0.1 \
    RABBIT_LOGIN=device \
    RABBIT_PASSWORD=device \
    RABBIT_VHOST=new_living_vhost

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py