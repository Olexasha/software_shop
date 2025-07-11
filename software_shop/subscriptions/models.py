from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TARIFF_DURATION_CHOICES = (
    (1, "День"),
    (7, "Неделя"),
    (31, "Месяц"),
    (365, "Год"),
)


class Tariff(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    description = models.TextField(verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    duration = models.IntegerField(
        choices=TARIFF_DURATION_CHOICES,
        verbose_name="Длительность",
        help_text="Длительность подписки в днях",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ["price"]


class UserSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Тариф",
    )
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата начала"
    )
    end_date = models.DateTimeField(verbose_name="Дата окончания")

    def __str__(self):
        return f"{self.user.username} - {self.tariff.name}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["start_date"]
        indexes = [
            models.Index(fields=["end_date"], name="end_date_index"),
        ]
