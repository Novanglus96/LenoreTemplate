import os
import re
import sys
from pathlib import Path
import requests


def get_version(tag):
    match = re.match(r"v?(\d+\.\d+\.\d+.*)", tag)
    return match.group(1) if match else tag.lstrip("v")


def main():
    tag = os.environ["COMMIT_TAG"]
    version = get_version(tag)
    changelog = os.environ["RELEASE_NOTES"]
    access_token = os.environ["PATREON_ACCESS_TOKEN"]
    campaign_id = os.environ["PATREON_CAMPAIGN_ID"]

    template = Path("scripts/patreon_post_template.html").read_text()
    content = template.format(version=version, changelog=changelog)

    title = f"{{PROJECT_NAME}} v{version} Released!"

    response = requests.post(
        "https://www.patreon.com/api/oauth2/v2/posts",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/vnd.api+json",
        },
        json={
            "data": {
                "type": "post",
                "attributes": {
                    "title": title,
                    "content": content,
                    "post_type": "text_only",
                    "is_paid": False,
                    "publish_status": "published",
                },
                "relationships": {
                    "campaign": {
                        "data": {
                            "type": "campaign",
                            "id": campaign_id,
                        }
                    }
                },
            }
        },
    )

    if response.status_code in (200, 201):
        data = response.json()
        post_id = data.get("data", {}).get("id", "unknown")
        print(f"✅ Posted to Patreon (post id: {post_id})")
    else:
        print(f"❌ Patreon API error {response.status_code}: {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
