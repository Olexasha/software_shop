from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductVariantViewSet, ProductViewSet, PurchaseViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"purchases", PurchaseViewSet, basename="purchases")

urlpatterns = [
    path(
        "product/<int:product_pk>/variants/",
        ProductVariantViewSet.as_view({"get": "list", "post": "create"}),
        name="variants",
    ),
    path(
        "product/<int:product_pk>/variants/<int:pk>/",
        ProductVariantViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="variant-detail",
    ),
    path("", include(router.urls)),
]
