from telegram import Update
from telegram.ext import ContextTypes
from bot.security import authorized, rate_limiter
from bot import config, code_backend
from bot.utils import send_response


@authorized
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["msg_count"] = 0
    await update.message.reply_text(
        "Claude Code on Telegram.\n\n"
        "Send any message and I'll handle it via Claude Code CLI.\n"
        f"Working directory: {config.WORKING_DIR}\n"
        "Follow-up messages continue the same conversation.\n\n"
        "/new — Start a fresh conversation\n"
    )


@authorized
async def new_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["msg_count"] = 0
    await update.message.reply_text("Fresh session started. Next message begins a new conversation.")


@authorized
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if not text:
        return

    if not rate_limiter.check(user_id):
        await update.message.reply_text("Rate limited. Please wait a moment.")
        return

    if context.user_data.get("processing"):
        await update.message.reply_text("Still processing your previous request...")
        return

    context.user_data["processing"] = True

    msg_count = context.user_data.get("msg_count", 0)
    is_continuation = msg_count > 0

    # Confirm we're working on it with a brief summary
    preview = text if len(text) <= 100 else text[:100] + "…"
    status = "Continuing" if is_continuation else "Working on"
    await update.message.reply_text(f"⏳ {status}: {preview}")
    await update.message.chat.send_action("typing")

    try:
        reply = await code_backend.send(user_id, text, is_continuation=is_continuation)
        context.user_data["msg_count"] = msg_count + 1
        await send_response(update, reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        context.user_data["processing"] = False
