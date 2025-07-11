from rest_framework import serializers

from .models import Product, ProductVariant, Purchase


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "is_active"]


class ProductVariantSerializer(serializers.ModelSerializer):
    version = serializers.ChoiceField(choices=ProductVariant.VERSION_CHOICES)

    class Meta:
        model = ProductVariant
        fields = "__all__"
        read_only_fields = ("id", "product")


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    product = serializers.SlugRelatedField(
        slug_field="name", queryset=Product.objects.all(), write_only=True
    )
    version = serializers.ChoiceField(
        choices=ProductVariant.VERSION_CHOICES, write_only=True
    )

    class Meta:
        model = Purchase
        fields = ["user", "product", "version", "purchase_date"]
        read_only_fields = ("user", "purchase_date")

    def create(self, validated_data):
        product = validated_data.pop("product")
        version = validated_data.pop("version")
        try:
            variant = ProductVariant.objects.get(
                product__name=product, version=version
            )
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError(
                f"Продукт '{product}' в версии '{version}' не существует."
            )
        validated_data["variant"] = variant
        return super().create(validated_data)
