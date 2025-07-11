from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.tg_bot.helpers import send_tg_congrats_with_subscription

from .models import Tariff, UserSubscription
from .serializers import TariffSerializer, UserSubscriptionSerializer


class TariffListView(viewsets.ReadOnlyModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    pagination_class = LimitOffsetPagination


class UserSubscriptionView(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["tariff__name"]
    search_fields = ["=tariff__name"]
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        tariff = get_object_or_404(
            Tariff, name=self.request.data.get("tariff")
        )
        start_date = timezone.now()
        end_date = timezone.now() + timedelta(days=tariff.duration)

        serializer.save(
            user=self.request.user,
            tariff=tariff,
            start_date=start_date,
            end_date=end_date,
        )

        if chat_id := self.request.user.tg_chat_id:
            send_tg_congrats_with_subscription(
                chat_id,
                self.request.user.username,
                start_date,
                end_date,
                tariff.name,
            )
