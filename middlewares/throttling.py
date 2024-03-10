from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

from templates.messages import MSG_THROTTLING_MIDDLEWARE


class ThrottlingMiddleware(BaseMiddleware):
    """
    Throttling middleware which is used as an anti-spam tool
    """

    def __init__(self, ttl=5):
        self.cache = TTLCache(maxsize=10_000, ttl=ttl)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:

        user = f'user{event.from_user.id}'

        if user in self.cache.keys():
            return await event.answer(MSG_THROTTLING_MIDDLEWARE)
        else:
            self.cache[user] = user
            return await handler(event, data)
