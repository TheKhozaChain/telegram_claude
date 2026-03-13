import os
import sys
from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    val = os.getenv(name)
    if not val:
        print(f"ERROR: Missing required env var: {name}")
        sys.exit(1)
    return val


TELEGRAM_BOT_TOKEN = _require("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = _require("ANTHROPIC_API_KEY")

ALLOWED_USER_IDS: set[int] = set()
raw_ids = os.getenv("ALLOWED_USER_IDS", "")
for uid in raw_ids.split(","):
    uid = uid.strip()
    if uid:
        ALLOWED_USER_IDS.add(int(uid))

if not ALLOWED_USER_IDS:
    print("ERROR: ALLOWED_USER_IDS must contain at least one Telegram user ID")
    sys.exit(1)

CLAUDE_CLI_PATH = os.getenv("CLAUDE_CLI_PATH", "claude")
RATE_LIMIT_CODE = int(os.getenv("RATE_LIMIT_CODE", "10"))
