from typing import Optional
import asyncio
import aiormq
import asyncio
import atexit
from aiormq.abc import DeliveredMessage
from aiormq.connection import Connection
from aiormq.channel import Channel
import json

URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "sample"


class MessageConsumer:
    def __init__(self, queue_name: str = QUEUE_NAME):
        self.queue_name = queue_name
        self.connection: Optional[Connection] = None
        self.channel: Optional[Channel] = None

        atexit.register(self.close_connection)

    @staticmethod
    def json_or_value(value):
        try:
            return json.loads(value)
        except Exception as error:
            # print(error)
            return value

    def close_connection(self):
        if self.connection != None:
            print("Closing connection")
            asyncio.run(self.connection.close())

    async def on_message_callback(self, message: DeliveredMessage):
        """
        on_message doesn't necessarily have to be defined as async.
        Here it is to show that it's possible.
        """

        print(f"[x] Received message: {self.json_or_value(message.body)}")

        # Represents async I/O operations
        await asyncio.sleep(3.0)

    async def start_consuming(self):
        # Perform connection
        self.connection = await aiormq.connect(url=URL)

        # Creating a channel
        self.channel = await self.connection.channel()

        # Declaring queue
        declare_ok = await self.channel.queue_declare(
            self.queue_name, auto_delete=True
        )

        consume_ok = await self.channel.basic_consume(
            declare_ok.queue, self.on_message_callback, no_ack=True
        )

        print(f" [*] Waiting for messages. To exit press CTRL+C")

        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            await self.connection.close()


if __name__ == "__main__":
    message_consumer = MessageConsumer()
    asyncio.run(message_consumer.start_consuming())
