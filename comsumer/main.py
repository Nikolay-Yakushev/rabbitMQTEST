import asyncio
import aio_pika
import json

from apps.core.counter import tasks_instance
from server_producer import loop_server


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://user1:user1@localhost:5672/vhost1", loop=loop
    )

    queue_name = "my_queue"

    async with connection:
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        while True:
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        msg = json.loads(message.body)
                        print(msg)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
