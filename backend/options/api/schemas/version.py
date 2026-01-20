from ninja import Schema
from pydantic import ConfigDict


# The class VersionOut is a schema for representing version information.
class VersionOut(Schema):
    id: int
    version_number: str

    model_config = ConfigDict(from_attributes=True)
