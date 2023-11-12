import logging
from websockets import WebSocketClientProtocol
from os import getenv

# module python-escpos
# from escpos.escpos import Escpos

# module pyescpos
from escpos.impl.epson import GenericESCPOS

async def handle_action(ws: WebSocketClientProtocol, p: GenericESCPOS, msg: dict):
    logging.debug(f"{type(msg)} | {msg}")

    for i in range(len(msg)):
        match msg[i]["action"]:
            case "text":
                p.text(msg[i]["content"])
            case "image":
                raise NotImplementedError
            case "cut": 
                p.text("\n\n\n")
                
        ws.send(str({"printer":getenv("fancy_name"), "action":msg[i]["action"], "content":msg[i]["content"], "status":"complete"}))