#!/usr/bin/env bash
set -euo pipefail

# Scaffold a new Lenore project from this template.
#
# Run this once, in a fresh clone of a repo created FROM this template on the
# forge (https://forge.lan.danielleandjohn.love/lenore).
#
# 🔑 WHAT CHANGED, AND WHY IT IS SHORTER THAN THE OLD ONE
# The previous version was GitHub-shaped: it pushed eight repo-level secrets
# from a .env.secrets file, set Actions permissions via `gh api`, and imported a
# branch ruleset. All three are gone:
#
#   * SECRETS are ORGANISATION secrets on `lenore`, inherited by every repo
#     through `secrets: inherit` in the workflow stubs. Nothing to set per repo,
#     so .env.secrets (and example_env_secrets) no longer exist. They are
#     managed in ansible-homelab: playbooks/forgejo_org_secrets.yml, sourced
#     from the vault.
#   * ACTIONS PERMISSIONS were a GitHub Actions concept. The GitHub runner fleet
#     was retired on 2026-08-10 and there are no GitHub workflows any more.
#   * THE RULESET still matters, but on the GitHub MIRROR rather than here — it
#     is what turns a mistaken merge on GitHub from silent data loss into a loud
#     mirror failure. scripts/rulesets/main.json is kept for exactly that, and
#     the checklist at the end says when to apply it.

die() { echo "❌ $*" >&2; exit 1; }

# ── Preconditions ────────────────────────────────────────────────────────────
command -v git >/dev/null 2>&1 || die "git is not installed."
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Not inside a git repository."

cd "$(git rev-parse --show-toplevel)"

# Refuse to run in the template itself. Substitution is destructive and there is
# no undo short of `git checkout .` — and the failure mode is silent, since a
# template with the placeholders already consumed still looks fine.
origin_url=$(git remote get-url origin 2>/dev/null || echo "")
case "$origin_url" in
  *LenoreTemplate*) die "This is the template repo itself. Create a new repo FROM the template first." ;;
esac

# ⚠️ init.sh is excluded here, not just in the substitution loop below: this
# file names the placeholders in its own comments, so a check that included it
# would always match and the "already run" guard would never fire.
git grep -qF "{{PROJECT_NAME}}" -- . ':!scripts/init.sh' >/dev/null 2>&1 \
  || die "No {{PROJECT_NAME}} placeholders found — init.sh has already been run here."

# ── Rename ───────────────────────────────────────────────────────────────────
read -r -p "Project name (e.g. LenoreApp): " PROJECT_NAME
read -r -p "Project slug (e.g. lenoreapp): " PROJECT_SLUG

[ -n "$PROJECT_NAME" ] || die "Project name cannot be empty."
[ -n "$PROJECT_SLUG" ] || die "Project slug cannot be empty."

# The slug becomes a Docker image name and a Postgres identifier, so constrain it
# rather than discovering the problem at the first `docker build`.
case "$PROJECT_SLUG" in
  [a-z0-9]*) ;;
  *) die "Slug must start with a lowercase letter or digit." ;;
esac
echo "$PROJECT_SLUG" | grep -qE '^[a-z0-9][a-z0-9_.-]*$' \
  || die "Slug may contain only lowercase letters, digits, '_', '.' and '-'."

# 🔑 `git grep -l` rather than `grep -rl`: it searches TRACKED FILES ONLY, so it
# cannot wander into .git/, node_modules/, .venv/ or dist/ the way the old
# `grep -rl ... . | xargs sed -i` did.
for placeholder_pair in "PROJECT_NAME:$PROJECT_NAME" "PROJECT_SLUG:$PROJECT_SLUG"; do
  key="${placeholder_pair%%:*}"
  value="${placeholder_pair#*:}"
  files=$(git grep -lF "{{$key}}" -- . ':!scripts/init.sh' || true)
  if [ -n "$files" ]; then
    echo "$files" | xargs sed -i "s/{{$key}}/$value/g"
  fi
done

echo "✅ Substituted {{PROJECT_NAME}} → $PROJECT_NAME, {{PROJECT_SLUG}} → $PROJECT_SLUG"

# ── Local files ──────────────────────────────────────────────────────────────
[ ! -f "$PROJECT_NAME.code-workspace" ] && [ -f code-workspace.example ] \
  && mv code-workspace.example "$PROJECT_NAME.code-workspace"
[ ! -f ".env" ] && [ -f example_env ] && mv example_env .env
[ ! -f ".env.dev" ] && [ -f example_env_dev ] && mv example_env_dev .env.dev

# ── Release branches ─────────────────────────────────────────────────────────
# .releaserc.json declares four channels (main/rc/beta/alpha). Nothing used to
# create the other three, so a new project had a four-channel config and one
# branch — and semantic-release only reveals that when someone tries to promote.
default_branch=$(git rev-parse --abbrev-ref HEAD)
for b in rc beta alpha; do
  if git show-ref --verify --quiet "refs/heads/$b"; then
    echo "ℹ️  branch $b already exists"
  else
    git branch "$b" "$default_branch"
    echo "✅ created branch $b"
  fi
done

# ── Dev environment ──────────────────────────────────────────────────────────
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --no-cache-dir -r backend/requirements.txt
pip install --no-cache-dir -r backend/requirements-dev.txt

if command -v npm >/dev/null 2>&1; then
  (cd frontend && npm install)
else
  echo "⚠️  npm not found — skipping frontend install."
fi

# ── What is left, and where it lives ─────────────────────────────────────────
cat <<EOF

────────────────────────────────────────────────────────────────────────────
$PROJECT_NAME is scaffolded. The rest is infrastructure, and it lives in
ansible-homelab rather than here:

  1. Commit and push, then push the release branches:
       git push -u origin $default_branch rc beta alpha

  2. Create the GitHub mirror repo (Novanglus96/$PROJECT_NAME), then add an
     entry to forgejo_push_mirror_repos in
     ansible-homelab/playbooks/group_vars/all/main.yml:

       - name: $PROJECT_NAME
         github: Novanglus96/$PROJECT_NAME

     and run:
       ansible-playbook playbooks/forgejo_push_mirrors.yml --ask-vault-pass

     That creates the push mirror with a Forgejo-generated SSH deploy key,
     registers the public half on GitHub, applies the +refs/notes/* refspec
     that semantic-release's channel bookkeeping depends on, and asserts the
     notes ref survives a sync.

  3. Apply the branch ruleset to the GITHUB mirror — this is the control that
     turns a mistaken merge there into a loud failure instead of a silent
     rewind of the forge's history:
       gh api --method POST repos/Novanglus96/$PROJECT_NAME/rulesets \\
         --input scripts/rulesets/main.json

  4. Add the repo to the release-audit list in lenore-ci's
     .forgejo/workflows/release-audit.yml (--repos-json), with --since-tag set
     to this project's first release.

Docs on the whole pipeline: https://wiki.danielleandjohn.love/home/home-lab/lenore-cicd
────────────────────────────────────────────────────────────────────────────
EOF
