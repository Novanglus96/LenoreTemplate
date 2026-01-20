from ninja import Router
from options.api.views.version import version_router

router = Router()
router.add_router("/", version_router)
