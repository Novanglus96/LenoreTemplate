from pathlib import Path

def get_version() -> str:
    version_file = (
        Path(__file__).resolve().parent.parent.parent / "VERSION"
    )
    return version_file.read_text().strip()