from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.tg_bot.helpers import send_tg_congarts_with_purchase

from .models import Product, ProductVariant, Purchase
from .permissions import IsAdminOrReadOnly
from .serializers import (
    ProductSerializer,
    ProductVariantSerializer,
    PurchaseSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).only(
        "id", "name", "description", "is_active"
    )
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]


class ProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductVariant.objects.filter(
            product__pk=self.kwargs["product_pk"]
        ).select_related("product")

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs["product_pk"])


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all().select_related(
        "variant__product", "user"
    )
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        purchase = serializer.save(user=self.request.user)
        if chat_id := self.request.user.tg_chat_id:
            send_tg_congarts_with_purchase(
                chat_id,
                self.request.user.username,
                f"{purchase.variant.product.name} - {purchase.variant.version.upper()}",
            )
