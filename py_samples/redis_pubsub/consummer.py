from typing import Any, Dict
import asyncio
from aredis_om import get_redis_connection
import json

URL = "redis://localhost:6379?decode_responses=True"


async def handler(message: Dict[str, Any]) -> None:
    try:
        print(json.loads(message["data"]))
    except json.JSONDecodeError:
        print(message)


async def consume():
    pubsub_channel = "sample"
    redis = get_redis_connection(url=URL)

    async with redis.pubsub(ignore_subscribe_messages=True) as ps:
        await ps.subscribe(pubsub_channel)
        async for msg in ps.listen():
            # {'type': 'message', 'pattern': None, 'channel': '...', 'data': '...'}
            if msg["type"] != "message":
                continue
            await handler(msg)


async def consume_thread():
    pubsub_channel = "sample"
    redis = get_redis_connection(url=URL)
    async with redis.pubsub(ignore_subscribe_messages=True) as ps:
        await ps.subscribe(**{pubsub_channel: handler})
        thread = None
        try:
            thread = await ps.run()
        except KeyboardInterrupt:
            # when it's time to shut it down...
            if thread != None:
                thread.stop()


if __name__ == "__main__":
    asyncio.run(consume())
