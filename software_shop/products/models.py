from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Введите описание продукта (необязательно)",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Отметьте, если продукт активен",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductVariant(models.Model):
    VERSION_BASIC = "basic"
    VERSION_PRO = "pro"
    VERSION_PREMIUM = "premium"

    VERSION_CHOICES = [
        (VERSION_BASIC, "Базовая"),
        (VERSION_PRO, "Профессиональная"),
        (VERSION_PREMIUM, "Премиум"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Продукт",
    )
    version = models.CharField(
        max_length=20, choices=VERSION_CHOICES, verbose_name="Версия"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    features = models.TextField(blank=True, verbose_name="Особенности")

    def __str__(self):
        return f"{self.product.name} — {self.get_version_display()}"

    class Meta:
        verbose_name = "Вариант продукта"
        verbose_name_plural = "Варианты продуктов"
        unique_together = ("product", "version")


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Пользователь",
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Вариант продукта",
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата покупки"
    )

    def __str__(self):
        return f"{self.user} купил {self.variant}"

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        ordering = ["-purchase_date"]
