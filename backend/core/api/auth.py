from django.contrib.auth import authenticate, login, logout
from ninja import Router, Schema
from django.http import HttpRequest
from django.middleware.csrf import get_token
from ninja.security import django_auth

router = Router(tags=["Accounts"])


class LoginIn(Schema):
    """
    Schema to represent a Login.

    Attributes:
        username (str): The username of the login.
        password (str): The password of the login.
    """

    username: str
    password: str


@router.post("/auth/login", auth=None)
def login_view(request: HttpRequest, payload: LoginIn):
    """
    The function `login_view` logs a user in.

    Endpoint:
        - **Path**: `/api/v1/auth/login`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.
        payload (LoginIn): A loginIn object.

    Returns:
        (dict): {success: True} if successful.
    """
    user = authenticate(
        request,
        username=payload.username,
        password=payload.password,
    )
    if not user:
        return 401, {"detail": "Invalid credentials"}

    login(request, user)
    return {"success": True}


@router.post("/auth/logout", auth=None)
def logout_view(request: HttpRequest):
    """
    The function `logout_view` logs out a user.

    Endpoint:
        - **Path**: `/api/v1/auth/logout`
        - **Method**: `POST`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (dict): {success: True} if successful.
    """
    logout(request)
    return {"success": True}


@router.get("/auth/csrf")
def csrf(request: HttpRequest):
    """
    The function `csrf` returns the csrf token.

    Endpoint:
        - **Path**: `/api/v1/auth/csrf`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (dict): {csrfToken: token} if successful.
    """
    return {"csrfToken": get_token(request)}


@router.get("/auth/me", auth=django_auth)
def me(request):
    """
    The function `me` retrieves logged in user.

    Endpoint:
        - **Path**: `/api/v1/auth/me`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (dict): {'username': username, 'is_staff': boolean} if successful
    """
    return {
        "username": request.user.username,
        "is_staff": request.user.is_staff,
    }
