#!/usr/bin/env bash
 set -e

# Check if gh cli is intalled
if ! command -v gh >/dev/null 2>&1; then
  echo "❌ GitHub CLI (gh) is not installed."
  echo "👉 Install it from https://cli.github.com/"
  exit 1
fi

# Check if jq cli is intalled
if ! command -v jq >/dev/null 2>&1; then
  echo "❌ jq is not installed."
  exit 1
fi

# Load .env.secrets
SECRETS_FILE=".env.secrets"
if [[ -f "$SECRETS_FILE" ]]; then
  while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" =~ ^# ]] && continue

    gh secret set "$key" --body "$value" >/dev/null
  done < "$SECRETS_FILE"
else
  echo "❌ .env.secrets not found. Create it before running init.sh"
  exit 1
fi

# Rename project
 read -p "Project name (e.g. LenoreApp): " PROJECT_NAME
 read -p "Project slug (e.g. lenoreapp): " PROJECT_SLUG

 grep -rl --exclude="init.sh" "{{PROJECT_NAME}}" . | xargs sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g"
 grep -rl --exclude="init.sh" "{{PROJECT_SLUG}}" . | xargs sed -i "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g"

# Set allow actions to approve pull requests
gh api \
  --method PUT \
  repos/Novanglus96/$PROJECT_NAME/actions/permissions/workflow \
  --input scripts/actions.json

# Import branch rulesets
# Check if a ruleset with the same name exists
EXISTS=$(gh api repos/Novanglus96/$PROJECT_NAME/rulesets \
  | jq -r --arg NAME "Protect Main" '.[] | select(.name==$NAME) | .name')

if [[ -n "$EXISTS" ]]; then
  echo "ℹ️ Ruleset '$RULESET_NAME' already exists in $REPO — skipping import."
else
  gh api \
  --method POST \
  repos/Novanglus96/$PROJECT_NAME/rulesets \
  --input scripts/rulesets/main.json
fi

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
 