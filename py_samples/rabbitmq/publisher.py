import aiormq
import asyncio

URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "sample"


class MessageQueue:
    def __init__(self, queue_name=QUEUE_NAME):
        self._connection_url = URL
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.declare_ok = None
        # atexit.register(self._close_connection)

    # def _close_connection(self):
    #     if self.connection != None:
    #         anyio.run(self.connection.close)

    async def __aenter__(self):
        self.connection = await aiormq.connect(self._connection_url)
        self.channel = await self.connection.channel()
        self.declare_ok = await self.channel.queue_declare(
            self.queue_name, auto_delete=True
        )
        return self

    async def __aexit__(self, *args, **kwargs):
        if self.connection != None:
            await self.connection.close()

    async def publish_message(self, message: bytes or str):
        if isinstance(message, str):
            message = message.encode()
        await self.channel.basic_publish(
            body=message, routing_key=self.queue_name, exchange=""
        )


async def main():
    async with MessageQueue() as mq:
        await mq.publish_message(message="foobar")


if __name__ == "__main__":
    asyncio.run(main())
