from django.contrib import admin

from .models import Product, ProductVariant, Purchase

admin.site.empty_value_display = "Не указано"
admin.site.site_header = "Продукты"


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "version", "price", "features")
    list_filter = ("product__name", "version")
    search_fields = ("product__name", "version")
    list_editable = ("price", "features")
    autocomplete_fields = ["product"]


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "variant", "purchase_date")
    list_filter = ("user__username", "variant__product__name", "purchase_date")
    search_fields = ("user__username", "variant__product__name")
    autocomplete_fields = ["user", "variant"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Purchase, PurchaseAdmin)
