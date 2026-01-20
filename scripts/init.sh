#!/usr/bin/env bash
 set -e

 read -p "Project name (e.g. LenoreApp): " PROJECT_NAME
 read -p "Project slug (e.g. lenoreapp): " PROJECT_SLUG

 grep -rl "{{PROJECT_NAME}}" . | xargs sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g"
 grep -rl "{{PROJECT_SLUG}}" . | xargs sed -i "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g"