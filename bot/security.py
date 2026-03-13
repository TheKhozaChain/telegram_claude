import time
import functools
from collections import defaultdict
from telegram import Update
from telegram.ext import ContextTypes
from bot import config


def authorized(func):
    """Decorator that restricts handler to allowed user IDs."""
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user or user.id not in config.ALLOWED_USER_IDS:
            if update.message:
                await update.message.reply_text("Unauthorized.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


class RateLimiter:
    def __init__(self):
        self._requests: dict[int, list[float]] = defaultdict(list)

    def check(self, user_id: int) -> bool:
        limit = config.RATE_LIMIT_CODE
        window = 60.0
        now = time.time()
        self._requests[user_id] = [t for t in self._requests[user_id] if now - t < window]
        if len(self._requests[user_id]) >= limit:
            return False
        self._requests[user_id].append(now)
        return True


rate_limiter = RateLimiter()
