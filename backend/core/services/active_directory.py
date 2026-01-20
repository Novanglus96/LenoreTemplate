from ms_active_directory import ADDomain
from django.conf import settings


def get_ad_domain_session():
    domain = ADDomain(settings.AD_DOMAIN)
    session = domain.create_session_as_user(
        settings.AD_USERNAME, settings.AD_PASSWORD
    )
    return session
