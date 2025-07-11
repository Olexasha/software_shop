import re
from http import HTTPStatus

from django.http import JsonResponse
from django.utils import timezone


class DoesUserHaveSubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if re.match(r"^/product/", request.path):
            if not request.user.subscriptions.exists():
                return JsonResponse(
                    {"detail": "У вас нет действующей подписки"},
                    status=HTTPStatus.FORBIDDEN,
                )
            users_subscriptions = request.user.subscriptions.first()
            now = timezone.now()
            if now >= users_subscriptions.end_date:
                return JsonResponse(
                    {
                        "detail": "У вас истекла подписка. Подпишитесь на новый тариф."
                    },
                    status=HTTPStatus.FORBIDDEN,
                )
        return response
