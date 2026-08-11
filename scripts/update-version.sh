#!/bin/bash
# Usage: ./scripts/update-version.sh <version>
# Updates version references across the project for a semantic-release prepare step.
#
# 🔴 Every path below must exist. `sed` on a missing file prints an error and
# carries on, and since the script ends with an `echo` it still exits 0 — so a
# stale path means a version reference silently stops being updated while the
# release reports success. Three paths were already wrong before the
# single-container rework: backend/Dockerfile and frontend/Dockerfile (now one
# Dockerfile at the repo root) and backend/api/fixtures/version.json (the app is
# `options`, not `api`). The guard below makes that class of drift loud.
#
# 🔴 Two things this script deliberately does NOT touch:
#   * backend/options/fixtures/version.json — its "__VERSION__" is a placeholder
#     that `manage.py load_version_fixture` substitutes from backend/VERSION at
#     load time. Writing a real version here consumes the placeholder and the
#     injection silently stops happening from then on.
#   * frontend/src/**.vue — the displayed version comes from
#     import.meta.env.VITE_APP_VERSION, which vite.config.js defines from
#     package.json. Updating package.json is what moves the UI.

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

VERSION_FILE="scripts/version.txt"
BACKEND_VERSION_FILE="backend/VERSION"
DOCKER_FILE="Dockerfile"
PACKAGE_JSON_FILE="frontend/package.json"

missing=0
for f in "$DOCKER_FILE" "$PACKAGE_JSON_FILE"; do
  if [ ! -f "$f" ]; then
    echo "ERROR: $f does not exist — update-version.sh is out of date with the repo"
    missing=1
  fi
done
[ "$missing" -eq 1 ] && exit 1

# backend/VERSION is the single source of truth at runtime: core/utils/version.py
# reads it for the API version, and load_version_fixture reads it to populate the
# Version model. It was never updated before this rework, so a released app
# reported 0.0.0 forever.
echo "$VERSION" > "$VERSION_FILE"
echo "$VERSION" > "$BACKEND_VERSION_FILE"
sed -i -r "s/^LABEL version=\"[^\"]*\"/LABEL version=\"$VERSION\"/" "$DOCKER_FILE"
sed -i -r "s/\"version\": \"[^\"]*\"/\"version\": \"$VERSION\"/" "$PACKAGE_JSON_FILE"

echo "Updated version to $VERSION"
