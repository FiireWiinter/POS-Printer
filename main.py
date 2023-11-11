import logging
import coloredlogs
import yaml

import asyncio
import websockets
import json

from escpos import config
from escpos.escpos import Escpos

from dotenv import load_dotenv
from os import getenv

from handler import handle_action
load_dotenv("config/.env")


def setup_logger():
    logger = logging.getLogger()
    with open("config/logging.yml", "r") as log_config:
        config = yaml.safe_load(log_config)
    coloredlogs.install(
        level="INFO",
        logger=logger,
        fmt=config["formats"]["console"],
        datefmt=config["formats"]["datetime"],
        level_styles=config["levels"],
        field_styles=config["fields"],
    )
    return logger


def setup_printer() -> Escpos:
    c = config.Config()
    c.load(config_path="config/printer.yml")
    return c.printer()

"""
async def handler(ws: websockets.WebSocketClientProtocol, p: escpos.Escpos):
    while True:
        try:
            msg = await ws.recv()
            msg = json.loads(msg)
            print(type(msg))


        except json.JSONDecodeError:
            await ws.send("ErrorJsonFormat")
        except websockets.ConnectionClosedOK:
            break
"""


async def main():
    p = setup_printer()
    headers = {
        "auth": getenv("website_auth"),
        "name": getenv("fancy_name")
    }
    async with websockets.connect(getenv("website_uri"), extra_headers=headers) as ws:
        while True:
            try:
                msg = await ws.recv()
                msg = json.loads(msg)
                await handle_action(ws, p, msg)
            except json.JSONDecodeError:
                await ws.send("ErrorJsonFormat")
            except websockets.ConnectionClosedOK:
                break



if __name__ == "__main__":
    try:
        setup_logger()
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        pass