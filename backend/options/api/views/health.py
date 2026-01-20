from ninja import Router

health_router = Router(tags=["Health"])


@health_router.get("/")
def health_check(request):
    """
    The function `health_check` returns ok if backend is ready.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        status (str): returns ok when backend is up
    """
    return {"status": "ok"}
