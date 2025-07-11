from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TariffListView, UserSubscriptionView

router = DefaultRouter()
router.register(r"tariffs", TariffListView, basename="tariffs")
router.register(r"subscription", UserSubscriptionView, basename="subscription")

urlpatterns = [
    path("", include(router.urls)),
]
