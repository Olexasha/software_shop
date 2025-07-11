from django.contrib import admin

from .models import Tariff, UserSubscription

admin.site.empty_value_display = "Не указано"
admin.site.site_header = "Подписки"


class TariffAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "tariff", "start_date", "end_date")
    list_filter = ("tariff", "start_date", "end_date")
    search_fields = ("user__username", "tariff__name")
    list_editable = ("end_date",)
    date_hierarchy = "start_date"


admin.site.register(Tariff, TariffAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
