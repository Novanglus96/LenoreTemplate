from ninja import Schema
from pydantic import ConfigDict


# The class VersionOut is a schema for representing version information.
class VersionOut(Schema):
    """
    Schema to represent a Version object.

    Attributes:
        id (int): ID of the Version object.
        version_number (str): The version number of the app.
    """

    id: int
    version_number: str

    model_config = ConfigDict(from_attributes=True)
