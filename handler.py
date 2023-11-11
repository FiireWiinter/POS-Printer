import logging
from websockets import WebSocketClientProtocol
from escpos.escpos import Escpos

async def handle_action(ws: WebSocketClientProtocol, p: Escpos, msg: dict):
    logging.debug(f"{type(msg)} | {msg}")
    for i in range(len(msg)):
        match msg[i]["action"]:
            case "text":
                p.text(msg[i]["content"])
            case "image":
                raise NotImplementedError
            case "cut": 
                p.cut()
                
        ws.send(str({"action":msg[i]["action"], "content":msg[i]["content"], "status":"complete"}))