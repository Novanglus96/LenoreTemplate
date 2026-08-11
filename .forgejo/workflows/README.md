# Forgejo workflow stubs

These are the CI a project scaffolded from this template inherits. All the real
logic lives once in `lenore/lenore-ci`, pinned at `@v1` — a moving major tag,
following the actions convention. A fix there reaches every repo without an edit
here; a breaking change gets a deliberate `@v2`. That is why these files are
~10 lines each, and it is why the template no longer carries eight full workflow
files that drift out of sync with the repos it templates.

| Stub | Calls | Fires on |
|---|---|---|
| `release.yml` | `release.yml@v1` | push to `main`/`rc`/`beta`/`alpha` |
| `build-publish.yml` | `build-publish.yml@v1` | `release: published`, or dispatch by tag |
| `docs.yml` | `docs.yml@v1` (`mode: preview`) | push to `main` |
| `docs-release.yml` | `docs.yml@v1` (`mode: release`) | `release: published`, or dispatch by tag |
| `announce.yml` | `announce.yml@v1` (`target: reddit`) | `release: published`, or dispatch by tag |
| `pr-title-lint.yml` | `pr-title-lint.yml@v1` | `pull_request` |
| `tests.yml` | `tests.yml@v1` | `pull_request` |

## 🔴 The template itself must never run these

Every stub ships live (`dry_run: false`) so a scaffolded project releases
without anyone editing a workflow file. The template repo is kept inert a
different way: **Actions is disabled on `lenore/LenoreTemplate`**, and that is
enforced by Ansible (`forgejo_push_mirrors.yml` reconciles `has_actions` on
every run) rather than left as a UI setting someone can flip and forget.

This replaces the old mechanism — an `if: github.repository !=
'Novanglus96/LenoreTemplate'` guard on all eight GitHub workflows. That guard
was never evaluated on Forgejo, and it fails *open*: if the expression does not
resolve, the comparison is true and the job runs. A control that has only ever
been tested on the platform you are leaving is not a control.

If Actions is ever enabled here, `release.yml` will cut real tags on the
template and `build-publish.yml` will fail on the unsubstituted
`{{PROJECT_SLUG}}` image name.

## 🔴 `.github/workflows/` is gone, and it must stay gone

Forgejo reads **both** `.github/workflows/` and `.forgejo/workflows/`. With
Actions enabled, restoring that directory means every workflow runs twice — and
two `semantic-release` instances on one push is precisely the double-changelog /
double-bump anomaly this migration exists to prevent.

## 🔴 Never merge on GitHub

GitHub is a **push mirror**, so a merge performed there is not a contribution —
it is a divergence. A `non_fast_forward` ruleset guards `main`/`rc`/`beta`/
`alpha` there, which converts that mistake from silent data loss into a loud,
detectable mirror failure. Land the work on the forge and let the mirror carry
it back. Issues stay on GitHub permanently; the forge's tracker is disabled.

## Secrets

Nothing needs setting per repo. `DOCKER_USERNAME`, `DOCKER_PASSWORD`,
`REDDIT_*`, `FORGE_TOKEN` and `HEALTHCHECKS_RELEASE_AUDIT` are **organisation
secrets on `lenore`**, inherited by every repo through `secrets: inherit` on the
stub. That is why `init.sh` no longer has an `.env.secrets` loop, and why
`example_env_secrets` was deleted. They are managed in Ansible
(`playbooks/forgejo_org_secrets.yml`), sourced from the vault.
