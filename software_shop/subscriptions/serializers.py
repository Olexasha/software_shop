from rest_framework import serializers
from subscriptions.models import Tariff, UserSubscription


class TariffNameField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(name=data)
        except Tariff.DoesNotExist:
            raise serializers.ValidationError(
                f"Тариф с названием '{data}' не существует."
            )


class TariffSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(
        style={"base_template": "textarea.html"}
    )
    is_active = serializers.BooleanField(
        default=True,
        help_text="Признак активности тарифа",
    )

    class Meta:
        model = Tariff
        fields = "__all__"
        read_only_fields = ["is_active"]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    tariff = TariffNameField(slug_field="name", queryset=Tariff.objects.all())

    class Meta:
        model = UserSubscription
        fields = "__all__"
        read_only_fields = ["user", "start_date", "end_date"]
