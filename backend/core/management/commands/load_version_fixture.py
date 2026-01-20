# backend/app/management/commands/load_version_fixture.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
import json
from pathlib import Path
import logging

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")


class Command(BaseCommand):
    help = "Load fixture with injected version from VERSION file"

    def handle(self, *args, **kwargs):
        version_path = (
            Path(__file__).resolve().parent.parent.parent.parent / "VERSION"
        )
        version = version_path.read_text().strip()

        fixture_path = Path("options/fixtures/version.json")
        data = json.loads(fixture_path.read_text())

        for item in data:
            if item["model"] == "options.Version":
                version_number = item["fields"].get("version_number")
                if version_number == "__VERSION__":
                    item["fields"]["version_number"] = version
                    task_logger.info(f"Setting version_number to {version}")

        tmp_path = Path("options/fixtures/_temp_app_metadata.json")
        tmp_path.write_text(json.dumps(data, indent=2))

        task_logger.info(
            f"Injecting version {version} into fixture and loading it..."
        )
        call_command("loaddata", str(tmp_path))

        tmp_path.unlink()  # Clean up
