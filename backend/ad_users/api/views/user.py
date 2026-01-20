from ninja import Router
from ninja.errors import HttpError
from ad_users.api.schemas.user import ADUserOut
from ad_users.services import (
    get_user_by_samaccountname,
    is_ad_user_enabled,
    get_ad_users,
)
from typing import List
import logging

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

ad_user_router = Router(tags=["AD Users"])


@ad_user_router.get("/get/{user_sam}", response=ADUserOut)
def get_ad_user(request, user_sam: str):
    """
    get_ad_user _summary_

    _extended_summary_

    Args:
        request (_type_): _description_
        user_sam (str): _description_

    Returns:
        _type_: _description_
    """

    user = get_user_by_samaccountname(user_sam)

    if not user:
        api_logger.error("AD User not found")
        raise HttpError(404, "User not found")

    api_logger.info(f"AD User {user_sam} found")
    return ADUserOut(
        username=user.get("sAMAccountName"),
        email=user.get("mail"),
        display_name=user.get("displayName"),
        enabled=is_ad_user_enabled(user),
        sid=user.get("objectSid"),
        when_changed=user.get("whenChanged"),
        given_name=user.get("givenName"),
        upn=user.get("userPrincipalName"),
        middle_name=user.get("middleName"),
        employee_id=user.get("employeeID"),
        department=user.get("department"),
        title=user.get("title"),
        manager=user.get("manager"),
        created_date=user.get("whenCreated"),
        last_logon=user.get("lastLogonTimestamp"),
        company=user.get("company"),
        description=user.get("description"),
        home_dir=user.get("homeDirectory"),
        home_drive=user.get("homeDrive"),
        initials=user.get("initials"),
        mobile=user.get("mobile"),
        office=user.get("physicalDeliveryOfficeName"),
        address=user.get("postalAddress"),
        zip=user.get("postalCode"),
        proxy_addresses=user.get("proxyAddresses"),
        pwd_last_set=user.get("pwdLastSet"),
        state=user.get("st"),
        street_address=user.get("streetAddress"),
        telephone=user.get("telephoneNumber"),
        script=user.get("scriptPath"),
        sn=user.get("sn"),
    )


@ad_user_router.get("/list", response=List[ADUserOut])
def get_all_ad_users(request):
    """
    get_ad_user _summary_

    _extended_summary_

    Args:
        request (_type_): _description_
        user_sam (str): _description_

    Returns:
        _type_: _description_
    """
    users = get_ad_users()
    schema_users = []

    if not users:
        api_logger.error("No users found!")
    api_logger.info("AD Users retreived")
    for user in users:
        schema_users.append(
            ADUserOut(
                username=user.get("sAMAccountName"),
                email=user.get("mail"),
                display_name=user.get("displayName"),
                enabled=is_ad_user_enabled(user),
            )
        )
    return schema_users
