import asyncio
from py_samples.redis_om.models import Sample
from aredis_om import Migrator, get_redis_connection

URL = "redis://localhost:6379?decode_responses=True"


async def main():
    redis_conn = get_redis_connection(url=URL)
    Sample.Meta.database = redis_conn

    await Migrator().run()

    async for t in await Sample.all_pks():
        print(await Sample.get(t))

    await redis_conn.close()


if __name__ == "__main__":
    asyncio.run(main())
