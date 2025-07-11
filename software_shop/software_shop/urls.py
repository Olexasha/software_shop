from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("subscriptions.urls")),
    path("", include("products.urls")),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]
