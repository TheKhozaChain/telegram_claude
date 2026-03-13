from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot import config, handlers


def main():
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("new", handlers.new_session))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))

    print(f"Bot starting. Allowed users: {config.ALLOWED_USER_IDS}")
    app.run_polling()


if __name__ == "__main__":
    main()
