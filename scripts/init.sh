#!/usr/bin/env bash
 set -e

# Rename project
 read -p "Project name (e.g. LenoreApp): " PROJECT_NAME
 read -p "Project slug (e.g. lenoreapp): " PROJECT_SLUG

 grep -rl --exclude="scripts/init.sh" "{{PROJECT_NAME}}" . | xargs sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g"
 grep -rl --exclude="scripts/init.sh" "{{PROJECT_SLUG}}" . | xargs sed -i "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g"

# Move example workspace
[ ! -f "$PROJECT_NAME.code-workspace" ] && mv code-workspace.example $PROJECT_NAME.code-workspace

# Move example env files
[ ! -f ".env" ] && mv example_env .env
[ ! -f ".env.dev" ] && mv example_env_dev .env.dev

# setup venv
[ ! -d .venv ] && python3 -m venv .venv

# activate venv
source .venv/bin/activate

# Install pip requirements
cd backend
pip install --no-cache-dir -r requirements.txt

# install npm packages
cd ../frontend
npm install
 