import logging
import coloredlogs
import yaml

import asyncio
import websockets
import json

# module escpos
# from escpos import config, printer
# from escpos.escpos import Escpos

# module pyescpos
from escpos import USBConnection
from escpos.impl.epson import GenericESCPOS

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


def printer_sys_msg(p: GenericESCPOS, msg: str):
    p.set_mode(emphasized=True, expanded=True)
    p.text_center(msg)
    p.set_mode(emphasized=False, expanded=False)
    p.lf(3)



def setup_printer() -> GenericESCPOS:
    # for python-escpos
    # c = config.Config()
    # c.load(config_path="config/printer.yml")
    # p = c.printer()
    # p.text("Printer detected!\n\n\n")
    # p.text("boo")
    # p.text("peek a boo")

    conn = USBConnection(0x0FE6, 0x811E, 0, 0x81, 0x01)
    p = GenericESCPOS(conn)
    p.init()
    printer_sys_msg(p, "Printer setup!")
    return p

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
        printer_sys_msg(p, "Connected to\nwebsocket!")
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