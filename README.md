# New Living - Led Ring
This is the IoT module software that is part of the New Living system. 
It allows you to run a program that communicates with the web application and is responsible for operating the LED ring. 
It allows displaying such animations as:
- Loading effect
- Eye effect
- Ambient mode

Docker container-based IoT modules make it easy to run software on any supported device without having to install and configure a local environment.

## System requirements
The only software you need to run is Docker.
The software has been tested on:
- Docker v20.10.21
- Raspberry Pi 4B (4GB RAM | chipset: Broadcom BCM2711 64-bit)
- LED Ring RGB WS2812B

## Usage
Use the following command to run the software:
```bash
docker run -d \
           --privileged \ 
           --network=host \ 
           -e SERVER_ADDRESS=<IP address of the server> \
           -e RABBIT_LOGIN=<username (RabbitMQ) > \
           -e RABBIT_PASSWORD=<user password (RabbitMQ)> \
           -e RABBIT_VHOST=<virtual host (RabbitMQ)> \
           -e LED_BRIGHTNESS=<led brightness in the range [0,1]>
```
After executing the above command, you can execute the `docker ps` command to check whether the container has been successfully launched.

If the container has not been started then run the `docker logs <container ID>` command to check the error that the software returned


## Contributing
If you want to make an additional IoT module for the New Living system:
- It is recommended to use the [Aio-pika](https://aio-pika.readthedocs.io/en/latest/) library (python3) or a renewal for another programming language to ensure asynchronicity and correct operation of the software.
- please contact the repository author 
- post your Docker image under the name <your username>/new-living-<module name> on [DockerHub](https://hub.docker.com/).

## License

[MIT](https://choosealicense.com/licenses/mit/)