from db import DBHandler
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes
from utils.tg_bot import logger
from utils.tg_bot.helpers import AuthState, create_access_token


async def send_start_keyboard(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    logger.info(
        "Отправка стартовой клавиатуры пользователю %s",
        update.effective_user.id,
    )
    keyboard = [[KeyboardButton("/start")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(
        "👋 Нажмите кнопку ниже, чтобы начать:", reply_markup=reply_markup
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Пользователь %s вызвал /start", update.effective_user.id)
    buttons = [
        [
            InlineKeyboardButton(
                "📱 Аутентификация по контакту", callback_data="by_contact"
            )
        ],
        [
            InlineKeyboardButton(
                "🔐 Аутентификация по логину и паролю",
                callback_data="by_password",
            )
        ],
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "*Выберите способ аутентификации:*",
        parse_mode="MarkdownV2",
        reply_markup=markup,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    logger.info(
        "Обработка выбора: %s от пользователя %s",
        query.data,
        update.effective_user.id,
    )

    if query.data == "by_contact":
        context.user_data["auth_state"] = AuthState.BY_TELEGRAM
        kb = [
            [KeyboardButton(text="📲 Отправить номер", request_contact=True)]
        ]
        reply_markup = ReplyKeyboardMarkup(
            kb, one_time_keyboard=True, resize_keyboard=True
        )
        await query.message.reply_text(
            "_Нажмите кнопку, чтобы поделиться номером телефона_ 📞",
            parse_mode="MarkdownV2",
            reply_markup=reply_markup,
        )

    elif query.data == "by_password":
        context.user_data["auth_state"] = AuthState.BY_CREDENTIALS
        await query.message.reply_text(
            "_Пожалуйста, введите логин и пароль через пробел:_ 🔑",
            parse_mode="MarkdownV2",
        )


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    logger.info(
        "Получен контактный номер: %s от %s",
        contact.phone_number,
        update.effective_user.id,
    )
    user = db.get_user_by_phone(contact.phone_number)

    if not user:
        logger.warning(
            "Пользователь с номером %s не найден", contact.phone_number
        )
        return await update.message.reply_text(
            "❌ Пользователь с таким номером не найден\\. Попробуйте снова\\."
        )

    logger.info("Пользователь найден: %s", user.get("username"))
    if not db.get_tg_username(user["id"]):
        logger.info("Пользователь уже аутентифицирован через Telegram")
        return await update.message.reply_text(
            "*Вы уже аутентифицированы через Telegram 🤖*",
            parse_mode="MarkdownV2",
        )

    db.set_tg_username(user["id"], update.effective_user.username)
    context.user_data["auth_user"] = user
    await update.message.reply_text(
        "✅ Телефон получен! Теперь введите ваш пароль 🔐"
    )


async def password_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("auth_state")
    user = None

    logger.info(
        "Обработка пароля от пользователя %s", update.effective_user.id
    )

    if state == AuthState.BY_TELEGRAM:
        user = context.user_data.get("auth_user")
        if not user:
            return await update.message.reply_text(
                "⚠️ Сначала отправьте номер телефона\\."
            )

        password = update.message.text
        success, tokens = create_access_token(user["username"], password)

        if not success:
            logger.warning(
                "Ошибка аутентификации по Telegram у %s: неверный пароль",
                user["username"],
            )
            return await update.message.reply_text(
                "*Неверный пароль 😕*", parse_mode="MarkdownV2"
            )

        db.set_tg_username(user["id"], update.effective_user.username)

    elif state == AuthState.BY_CREDENTIALS:
        try:
            username, password = update.message.text.split()
        except ValueError:
            return await update.message.reply_text(
                "❗ Пожалуйста, введите логин и пароль через пробел."
            )

        success, tokens = create_access_token(username, password)
        if not success:
            logger.warning("Ошибка аутентификации по кредам у %s", username)
            return await update.message.reply_text(
                "*Неверный логин или пароль 😕*", parse_mode="MarkdownV2"
            )
        user = db.get_user_by_username(username)

    db.set_tg_chat_id(user.get("username"), update.effective_user.id)
    logger.info(
        "Пользователь %s успешно аутентифицирован", user.get("username")
    )
    await update.message.reply_text(
        f"*🎉 Вы успешно аутентифицированы\\!*\n\n_Ваш токен:_\n```{tokens['access']}```",
        parse_mode="MarkdownV2",
    )
    context.user_data.clear()


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Неизвестная команда от пользователя %s", update.effective_user.id
    )
    keyboard = [[KeyboardButton("/start")]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(
        "🤖 Я не понял вашу команду\\.\nПожалуйста, нажмите кнопку ниже, чтобы начать:",
        parse_mode="MarkdownV2",
        reply_markup=reply_markup,
    )


db = DBHandler()
