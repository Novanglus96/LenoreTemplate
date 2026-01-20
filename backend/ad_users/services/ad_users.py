from core.services.active_directory import get_ad_domain_session


def user_ad_attributes():
    return [
        "mail",
        "displayName",
        "givenName",
        "sAMAccountName",
        "userAccountControl",
        "userPrincipalName",
        "middleName",
        "employeeID",
        "department",
        "title",
        "manager",
        "whenCreated",
        "lastLogonTimestamp",
        "company",
        "description",
        "homeDirectory",
        "homeDrive",
        "initials",
        "mobile",
        "physicalDeliveryOfficeName",
        "postalAddress",
        "postalCode",
        "proxyAddresses",
        "pwdLastSet",
        "st",
        "streetAddress",
        "telephoneNumber",
        "scriptPath",
        "whenChanged",
        "objectSid",
        "sn",
    ]


def get_user_by_samaccountname(sam: str):
    session = get_ad_domain_session()

    user = session.find_user_by_sam_name(
        sam,
        user_ad_attributes(),
    )

    return user if user else None


def is_ad_user_enabled(user) -> bool:
    uac = int(user.get("userAccountControl", 0))
    return not (uac & 2)


def get_ad_users():
    session = get_ad_domain_session()

    users = session.find_users_by_attribute(
        "objectCategory",
        "CN=Person,CN=Schema,CN=Configuration,DC=middletownnj,DC=local",
        user_ad_attributes(),
    )

    return users
