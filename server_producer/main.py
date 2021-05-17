import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from apps.producer.views import v1_route
from uvicorn import Config, Server

from server_producer import loop_server


def _get_app():
    _app = FastAPI()
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    _app.include_router(v1_route)

    return _app


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(filename="my_dotenv.env.dev"))
    config = Config(app=_get_app(), loop=loop_server)
    server = Server(config)
    loop_server.run_until_complete(server.serve())
