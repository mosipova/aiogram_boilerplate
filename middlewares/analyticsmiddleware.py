import logging
from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class AnalyticsMiddleware(BaseMiddleware):
    """
    Middleware to log something before handling event
    """

    def __init__(self, conn):
        self.conn = conn

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        msg_json = event.model_dump_json()
        # await insert_log_data(self.conn, msg_json)
        logging.info(f'analytics middleware: {msg_json}')

        return await handler(event, data)
