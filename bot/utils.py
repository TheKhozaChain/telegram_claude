from telegram import Update

MAX_MSG_LEN = 4096
MAX_TOTAL_LEN = 20000


def split_message(text: str, max_len: int = MAX_MSG_LEN) -> list[str]:
    """Split text into chunks that fit Telegram's message limit."""
    if not text:
        return ["(empty response)"]

    # Truncate very long output
    if len(text) > MAX_TOTAL_LEN:
        text = text[:MAX_TOTAL_LEN] + f"\n\n[Truncated — {len(text)} chars total]"

    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break

        # Try to split at a double newline
        split_at = text.rfind("\n\n", 0, max_len)
        if split_at == -1:
            # Try single newline
            split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            # Try space
            split_at = text.rfind(" ", 0, max_len)
        if split_at == -1:
            # Hard cut
            split_at = max_len

        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    return chunks


async def send_response(update: Update, text: str):
    """Send a potentially long response as multiple messages."""
    chunks = split_message(text)
    for chunk in chunks:
        try:
            await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception:
            # Fallback to plain text if Markdown parsing fails
            await update.message.reply_text(chunk)
