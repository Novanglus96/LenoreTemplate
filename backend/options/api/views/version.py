from ninja import Router
from ninja.errors import HttpError
from options.models import Version
from options.api.schemas.version import VersionOut
from django.shortcuts import get_object_or_404
import logging
from django.http import Http404

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

version_router = Router(tags=["Version"])


@version_router.get("/list", response=VersionOut)
def list_version(request):
    """
    The function `list_version` retrieves the version.

    Endpoint:
        - **Path**: `/api/v1/options/version/list`
        - **Method**: `GET`

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        (VersionOut): A version object.
    """

    try:
        qs = get_object_or_404(Version, id=1)
        api_logger.debug("Version retrieved")
        return qs
    except Http404:
        raise
    except Exception as e:
        # Log other types of exceptions
        api_logger.error("Version not retrieved")
        error_logger.error(f"{str(e)}")
        raise HttpError(500, "Record retrieval error")
