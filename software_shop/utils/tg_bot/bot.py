from handlers import *
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from utils.tg_bot import TOKEN, logger


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    logger.info("Бот запущен")

    app.add_handler(CommandHandler("hello", send_start_keyboard))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), password_handler)
    )
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    app.run_polling()


if __name__ == "__main__":
    main()
