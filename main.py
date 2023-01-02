import json

import neopixel
import board
import asyncio
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from colour import Color
import uuid

NUMBER_OF_PIX = 12
PIX_PIN = board.D18
START_COLOR = [255, 255, 255]
OFF_COLOR = [0, 0, 0]
DEVICE_MAC_ADDRESS = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
DEFAULT_OFF_TEMPLATE = {
    'device_status': 'ON',
    'ambient': 'OFF',
    'eye': {
        'status': 'OFF',
        'color': OFF_COLOR
    },
    'loading': {
        'status': 'OFF',
        'color': OFF_COLOR
    }
}


def check_equality_of_macs(first_mac: str, second_mac: str) -> bool:
    one = first_mac.split(':')
    if '-' in second_mac:
        two = second_mac.split('-')
    else:
        two = second_mac.split(':')

    two = list(map(str.lower, two))

    return one == two


with neopixel.NeoPixel(PIX_PIN, NUMBER_OF_PIX, brightness=.2, auto_write=False) as pixels:
    async def on_message(message: AbstractIncomingMessage) -> None:
        decoded_message = json.loads(message.body)

        if not check_equality_of_macs(DEVICE_MAC_ADDRESS, decoded_message['device']['mac']):
            return

        if decoded_message['change']['mode'] == 'TURN_ON':
            decoded_message['actual_status'] = DEFAULT_OFF_TEMPLATE
            decoded_message['actual_status']['loading']['status'] = 'ON'
            decoded_message['actual_status']['loading']['color'] = START_COLOR

            pixels.fill(OFF_COLOR)
            pixels.show()
            kill_task('current_loop')
            asyncio.create_task(eye(START_COLOR), name='current_loop')
        elif decoded_message['change']['mode'] == 'TURN_OFF':
            decoded_message['actual_status'] = DEFAULT_OFF_TEMPLATE
            decoded_message['actual_status']['device_status'] = 'OFF'

            pixels.fill(OFF_COLOR)
            pixels.show()
        elif decoded_message['change']['mode'] == 'AMBIENT':
            decoded_message['actual_status'] = DEFAULT_OFF_TEMPLATE
            decoded_message['actual_status']['ambient'] = 'ON'

            pixels.fill(OFF_COLOR)
            pixels.show()
            kill_task('current_loop')
            asyncio.create_task(ambient(), name='current_loop')
        elif decoded_message['change']['mode'] == 'EYE':
            decoded_message['actual_status'] = DEFAULT_OFF_TEMPLATE
            decoded_message['actual_status']['eye']['status'] = 'ON'
            color = decoded_message['change']['options']['color']
            decoded_message['actual_status']['eye']['color'] = color

            pixels.fill(OFF_COLOR)
            pixels.show()
            kill_task('current_loop')
            asyncio.create_task(eye(color), name='current_loop')
        elif decoded_message['change']['mode'] == 'LOADING':
            decoded_message['actual_status'] = DEFAULT_OFF_TEMPLATE
            decoded_message['actual_status']['loading']['status'] = 'ON'
            color = decoded_message['change']['options']['color']
            decoded_message['actual_status']['loading']['color'] = color

            pixels.fill(OFF_COLOR)
            pixels.show()
            kill_task('current_loop')
            asyncio.create_task(loading(color), name='current_loop')

        await message.ack()

        decoded_message.pop('change')

        await message.channel.basic_publish(json.dumps(decoded_message).encode(), routing_key='*',
                                            exchange='device_status_exchange')

        await asyncio.sleep(2)


    def kill_task(name: str) -> None:
        tasks = asyncio.all_tasks()
        for task in tasks:
            if task.get_name() == name:
                task.cancel()


    async def loading(color: list[int, int, int]) -> None:
        global NUMBER_OF_PIX

        while True:
            for i in range(NUMBER_OF_PIX):
                pixels[i] = color
                pixels[(i + NUMBER_OF_PIX - 4) % NUMBER_OF_PIX] = OFF_COLOR
                pixels.show()
                await asyncio.sleep(0.08)


    async def ambient() -> None:
        global NUMBER_OF_PIX

        red_color = Color('red')
        magenta_color = Color('magenta')
        colors = list(red_color.range_to(magenta_color, 100))
        colors_reverse = colors.copy()
        colors_reverse.reverse()

        while True:
            for color in colors:
                pixels.fill([
                    int(color.get_red() * 255),
                    int(color.get_green() * 255),
                    int(color.get_blue() * 255)
                ])
                pixels.show()
                await asyncio.sleep(0.05)
            for color in colors_reverse:
                pixels.fill([
                    int(color.get_red() * 255),
                    int(color.get_green() * 255),
                    int(color.get_blue() * 255)
                ])
                pixels.show()
                await asyncio.sleep(0.05)


    async def eye(color: list[int, int, int]) -> None:
        global NUMBER_OF_PIX
        offset = 0
        while True:
            i = 0
            t = 0
            for i in range(0, NUMBER_OF_PIX):
                c = 0
                if ((offset + i) & 7) < 2:
                    c = color
                pixels[i] = c
                pixels[(NUMBER_OF_PIX - 1) - i] = c
            pixels.write()
            offset += 1
            await asyncio.sleep(0.1)
            await asyncio.sleep(0.01)


    async def main() -> None:
        connection = await connect(
            host='192.168.1.12',
            login='device',
            password='device',
            virtualhost='new_living_vhost'
        )
        async with connection:
            asyncio.create_task(loading(START_COLOR), name='current_loop')

            channel = await connection.channel()

            queue = await channel.get_queue('change_parameter_queue')

            await queue.consume(on_message, no_ack=False)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            await asyncio.Future()


    if __name__ == '__main__':
        asyncio.run(main())
