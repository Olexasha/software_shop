from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product, ProductVariant


@receiver(post_save, sender=Product)
def create_default_variant(sender, instance, created, **kwargs):
    if created and not instance.variants.exists():
        ProductVariant.objects.create(
            product=instance,
            version=ProductVariant.VERSION_BASIC,
            price=0,
            features="Базовая версия по умолчанию",
        )


@receiver(post_save, sender=Product)
def before_product_creating(sender, instance, **kwargs):
    print("Добавляется продукт:", instance.name)
