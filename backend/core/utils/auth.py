from ninja.security import HttpBearer
from decouple import config
from django.conf import settings


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        """
        The `authenticate` function authenticates the api endpoint.

        Args:
            request (HTTPRequest): The http request.
            token (): CSRF Token

        Returns:
            (dict): {'type': api_key, 'name': service-account}
        """
        api_key = getattr(settings, "VITE_API_KEY", None) or config(
            "VITE_API_KEY", default=None
        )

        if api_key and token == api_key:
            return {
                "type": "api_key",
                "name": "service-account",
            }
