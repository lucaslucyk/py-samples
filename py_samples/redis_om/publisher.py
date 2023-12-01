import asyncio
from py_samples.redis_om.models import Sample
from aredis_om import Migrator, get_redis_connection

URL = "redis://localhost:6379?decode_responses=True"


async def main():
    redis_conn = get_redis_connection(url=URL)
    Sample.Meta.database = redis_conn

    await Migrator().run()

    sample = Sample(foo="Foo", bar="Bar")
    sample = await sample.save()
    print(sample)


if __name__ == "__main__":
    asyncio.run(main())