from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    tg_username = models.CharField(
        max_length=50, blank=True, verbose_name="Telegram"
    )
    tg_chat_id = models.BigIntegerField(
        null=True, blank=True, verbose_name="ID чата"
    )

    def __str__(self):
        return self.username
