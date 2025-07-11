import os

from django.conf import settings
from sqlalchemy import MetaData, Table, create_engine, select, update
from sqlalchemy.orm import sessionmaker
from utils.tg_bot import logger


class DBHandler:
    DB_HOST = os.getenv("DB_HOST", settings.DATABASES["default"]["HOST"])
    DB_PORT = os.getenv("DB_PORT", settings.DATABASES["default"]["PORT"])
    DB_NAME = os.getenv("DB_NAME", settings.DATABASES["default"]["NAME"])
    DB_USER = os.getenv("DB_USER", settings.DATABASES["default"]["USER"])
    DB_PASSWORD = os.getenv(
        "DB_PASSWORD", settings.DATABASES["default"]["PASSWORD"]
    )
    DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(DB_URL)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    users = Table("users_customuser", metadata, autoload_with=engine)
    subscriptions = Table(
        "subscriptions_usersubscription", metadata, autoload_with=engine
    )

    def get_user_by_phone(self, phone):
        logger.debug("Поиск пользователя по телефону: %s", phone)
        with self.SessionLocal() as session:
            return (
                session.execute(
                    select(self.users).where(self.users.c.phone == phone)
                )
                .mappings()
                .first()
            )

    def get_user_by_username(self, username):
        logger.debug("Поиск пользователя по username: %s", username)
        with self.SessionLocal() as session:
            return (
                session.execute(
                    select(self.users).where(self.users.c.username == username)
                )
                .mappings()
                .first()
            )

    def get_user_by_tg_username(self, tg_username):
        logger.debug(
            "Поиск пользователя по Telegram username: %s", tg_username
        )
        with self.SessionLocal() as session:
            return (
                session.execute(
                    select(self.users).where(
                        self.users.c.tg_username == tg_username
                    )
                )
                .mappings()
                .first()
            )

    def get_tg_username(self, user_id):
        logger.debug(
            "Проверка Telegram username у пользователя ID: %s", user_id
        )
        with self.SessionLocal() as session:
            return (
                session.execute(
                    select(self.users).where(self.users.c.id == user_id)
                )
                .mappings()
                .first()
            )

    def set_tg_username(self, user_id, tg_username):
        logger.info(
            "Установка Telegram username '%s' для пользователя ID: %s",
            tg_username,
            user_id,
        )
        with self.SessionLocal() as session:
            session.execute(
                update(self.users)
                .where(self.users.c.id == user_id)
                .values(tg_username=tg_username)
            )
            session.commit()

    def set_tg_chat_id(self, username, chat_id):
        logger.info(
            "Привязка chat_id %d к пользователю '%s'", chat_id, username
        )
        with self.SessionLocal() as session:
            session.execute(
                update(self.users)
                .where(self.users.c.username == username)
                .values(tg_chat_id=chat_id)
            )
            session.commit()
