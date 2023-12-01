from asyncio.exceptions import TimeoutError, CancelledError
import asyncio
from aredis_om import get_redis_connection

URL = "redis://localhost:6379?decode_responses=True"


async def publish():
    pubsub_channel = "sample"
    message = "foobar"
    redis = get_redis_connection(url=URL)
    try:
        r = await redis.publish(pubsub_channel, message)
    except (ConnectionError, TimeoutError, CancelledError) as err:
        print(err)


if __name__ == "__main__":
    asyncio.run(publish())
