from ninja import Router
from ad_users.api.views.user import ad_user_router

router = Router()
router.add_router("/", ad_user_router)
