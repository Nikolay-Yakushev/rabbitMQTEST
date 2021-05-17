from typing import Callable

import aio_pika
from fastapi import APIRouter
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response
from apps.core.counter import tasks_instance
# from apps.core.counter import TASKS


from apps.producer.schemas import IncomingMessage


class RabbitMqRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            connection = await aio_pika.connect_robust(
                url='amqp://user1:user1@localhost:5672/vhost1')
            request.state.connection = connection
            response: Response = await original_route_handler(request)
            return response

        return custom_route_handler


v1_route = APIRouter(route_class=RabbitMqRoute)


@v1_route.post("/add_task")
async def add_task(model: IncomingMessage,
                   request: Request):
    routing_key = "my_queue"
    async with request.state.connection as connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=model.json().encode()),
            routing_key=routing_key,
        )
        await tasks_instance.add_tasks_completed()


@v1_route.get("/get_stats")
async def get_stats():
    tasks_amount = await tasks_instance.get_tasks()
    return {"task completed": tasks_amount}
