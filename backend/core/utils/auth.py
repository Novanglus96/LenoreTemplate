from ninja.security import HttpBearer
from decouple import config
from django.conf import settings


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        api_key = getattr(settings, "VITE_API_KEY", None) or config(
            "VITE_API_KEY", default=None
        )

        if api_key and token == api_key:
            return {
                "type": "api_key",
                "name": "service-account",
            }
