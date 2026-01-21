#!/usr/bin/env bash
 set -e

# Check if gh cli is intalled
if ! command -v gh >/dev/null 2>&1; then
  echo "❌ GitHub CLI (gh) is not installed."
  echo "👉 Install it from https://cli.github.com/"
  exit 1
fi

# Load .env.secrets
if [[ -f .env.secrets ]]; then
  set -a
  source .env.secrets
  set +a
else
  echo "❌ .env.secrets not found. Create it before running init.sh"
  exit 1
fi

# Rename project
 read -p "Project name (e.g. LenoreApp): " PROJECT_NAME
 read -p "Project slug (e.g. lenoreapp): " PROJECT_SLUG

 grep -rl --exclude="scripts/init.sh" "{{PROJECT_NAME}}" . | xargs sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g"
 grep -rl --exclude="scripts/init.sh" "{{PROJECT_SLUG}}" . | xargs sed -i "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g"

# Set allow actions to approve pull requests
gh api \
  --method PUT \
  repos/Novanglus96/$PROJECT_NAME/actions/permissions \
  -f enabled=true \
  -f allowed_actions="all" \
  -f allow_actions_to_approve_pull_requests=true


# Import branch rulesets
gh api \
  --method POST \
  repos/Novanglus96/$PROJECT_NAME/rulesets \
  --input scripts/rulesets/main.json

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
 