from ninja import Schema
from typing import Optional, List
from datetime import datetime


class ADUserOut(Schema):
    username: str
    enabled: bool
    when_changed: datetime
    sid: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    upn: Optional[str] = None
    middle_name: Optional[str] = None
    employee_id: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    manager: Optional[str] = None
    created_date: Optional[datetime] = None
    last_logon: Optional[datetime] = None
    company: Optional[str] = None
    description: Optional[str] = None
    home_dir: Optional[str] = None
    home_drive: Optional[str] = None
    initials: Optional[str] = None
    mobile: Optional[str] = None
    office: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    proxy_addresses: Optional[List[str]] = None
    pwd_last_set: Optional[datetime] = None
    state: Optional[str] = None
    street_address: Optional[str] = None
    telephone: Optional[str] = None
    script: Optional[str] = None
    sn: Optional[str] = None
