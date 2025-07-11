import re
from http import HTTPStatus

import requests
from django.conf import settings
from utils.tg_bot import TOKEN, logger


class AuthState:
    BY_TELEGRAM = "await_contact"
    BY_CREDENTIALS = "await_credentials"


def create_access_token(username, password):
    response = requests.post(
        f"http://{settings.DJANGO_APP_NAME}:{settings.DJANGO_APP_PORT}/jwt/create/",
        json={"username": username, "password": password},
    )
    return response.status_code == HTTPStatus.OK, (
        response.json() if response.status_code == HTTPStatus.OK else {}
    )


def escape_markdown(text: str) -> str:
    escape_chars = r"[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


def send_message(chat_id, text):
    text_parsed = escape_markdown(text)
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text_parsed,
            "parse_mode": "MarkdownV2",
        },
    )
    logger.info(response.json())


def send_tg_congarts_with_purchase(chat_id, username, product_name):
    text = (
        f"🎉 *{username}, спасибо за покупку!* 🎉\n\n"
        f"🛍️ _Товар:_ *{product_name}*\n\n"
        f"Надеемся, вам понравится! 😊"
    )
    logger.info(
        "Отправка поздравления с покупкой пользователю '%s' (%s)",
        username,
        product_name,
    )
    send_message(chat_id, text)


def send_tg_congrats_with_subscription(
    chat_id, username, start_date, end_date, subscription_name
):
    text = (
        f"🎉 *{username}, вы оформили подписку!* 🎉\n\n"
        f"📦 _Подписка:_ *{subscription_name}*\n"
        f"📅 _Начало:_ *{start_date}*\n"
        f"📅 _Конец:_ *{end_date}*\n\n"
        f"Спасибо, что вы с нами! 💖"
    )
    logger.info(
        "Отправка поздравления с подпиской пользователю '%s': %s с %s по %s",
        username,
        subscription_name,
        start_date,
        end_date,
    )
    send_message(chat_id, text)
