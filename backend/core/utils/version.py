from pathlib import Path


def get_version() -> str:
    """
    The `get_version` function return the version from the version file.

    Returns:
        str: The version of the app from the version file.
    """
    version_file = Path(__file__).resolve().parent.parent.parent / "VERSION"
    return version_file.read_text().strip()
