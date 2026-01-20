from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_cryptography.fields import encrypt

# Create your models here.


class ActiveDirectoryUser(models.Model):
    """
    Model representing an account type for categorizing accounts.

    Fields:
    - account_type (CharField): The name of the account type, limited to 254 characters,
    and must be unique.
    - color (CharField): The color associated with accounts of this type, default is #059669.
    - icon (CharField): The icon associciated with accounts of this type, limited to 25
    characters.
    """

    sam_account = encrypt(models.CharField(max_length=254))
    email = models.CharField(max_length=254, unique=True)
    display_name = models.CharField(max_length=508)
    enabled = models.BooleanField(default=True)
    sid = models.CharField(max_length=508, unique=True)
    when_changed = models.DateTimeField()
    given_name = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    upn = models.CharField(max_length=508, null=True, default=None, blank=True)
    middle_name = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    employee_id = models.IntegerField(null=True, default=None, blank=True)
    department = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    title = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    manager = models.CharField(
        max_length=508, null=True, default=None, blank=True
    )
    created_date = models.DateTimeField(default=None, blank=True, null=True)
    last_logon = models.DateTimeField(default=None, blank=True, null=True)
    company = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    description = models.CharField(
        max_length=508, null=True, default=None, blank=True
    )
    home_dir = models.CharField(
        max_length=508, null=True, default=None, blank=True
    )
    home_drive = models.CharField(
        max_length=10, null=True, default=None, blank=True
    )
    initials = models.CharField(
        max_length=3, null=True, default=None, blank=True
    )
    mobile = models.CharField(
        max_length=25, null=True, default=None, blank=True
    )
    office = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    address = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    zip_code = models.CharField(
        max_length=5, null=True, default=None, blank=True
    )
    proxy_addresses = ArrayField(
        models.CharField(max_length=254), blank=True, default=list, null=True
    )
    pwd_last_set = models.DateTimeField(default=None, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, default=None, blank=True)
    street_address = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    telephone = models.CharField(
        max_length=25, null=True, default=None, blank=True
    )
    script = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )
    sur_name = models.CharField(
        max_length=254, null=True, default=None, blank=True
    )

    def __str__(self):
        return self.display_name
