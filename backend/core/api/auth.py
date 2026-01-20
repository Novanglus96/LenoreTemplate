from django.contrib.auth import authenticate, login, logout
from ninja import Router, Schema
from django.http import HttpRequest
from django.middleware.csrf import get_token
from ninja.security import django_auth

router = Router(tags=["Accounts"])


class LoginIn(Schema):
    username: str
    password: str


@router.post("/auth/login", auth=None)
def login_view(request: HttpRequest, payload: LoginIn):
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
    logout(request)
    return {"success": True}


@router.get("/auth/csrf")
def csrf(request: HttpRequest):
    return {"csrfToken": get_token(request)}


@router.get("/auth/me", auth=django_auth)
def me(request):
    return {
        "username": request.user.username,
        "is_staff": request.user.is_staff,
    }
