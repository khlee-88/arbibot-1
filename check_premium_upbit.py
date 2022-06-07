import websockets
import asyncio
import json
from pprint import pprint

async def upbit_ws_client():
    uri = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(uri,  ping_interval=60) as websocket:
        subscribe_fmt = [
            {"ticket":"test"},
            {
                "type": "orderbook",
                "codes":["KRW-XRP"],
                "isOnlyRealtime": True
            },
            {"format":"SIMPLE"}
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)

async def bithumb_ws_client():
    uri = "wss://pubwss.bithumb.com/pub/ws"

    async with websockets.connect(uri, ping_interval=None) as websocket:
        greeting = await websocket.recv()
        print(greeting)

        subscribe_fmt = {
            "type":"orderbookdepth",
            "symbols": ["XRP_KRW"],
            "tickTypes": ["1H"]
        }
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            pprint(data)

async def main():

    tasks = [
        asyncio.ensure_future(upbit_ws_client()),
        asyncio.ensure_future(bithumb_ws_client())
    ]

    await upbit_ws_client()
    await bithumb_ws_client()
asyncio.run(main())