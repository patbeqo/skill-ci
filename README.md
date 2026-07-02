# skill-ci

Shared CI for Temporal **skill** repos. Hosts a reusable GitHub Actions workflow
that packages a skill and syncs it into the plugin repos
(`cursor-temporal-plugin`, `codex-temporal-plugin`, `claude-temporal-plugin`).

## Usage

In a skill repo (named `skill-<name>`), add `.github/workflows/package-skill.yml`:

```yaml
name: Package and Sync Skill

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  package-and-sync:
    uses: temporalio/skill-ci/.github/workflows/package-and-sync.yml@v1
    permissions:
      contents: write
    secrets: inherit
    # with:
    #   excludes: ".git .github .gitignore .DS_Store *.zip README.md"
```

That's the entire caller. The reusable workflow derives the skill name from the
caller repo's name (dropping the `skill-` prefix), reads the version from
`SKILL.md`, cuts a release when it changes, and opens sync PRs against the
plugin repos.

### Inputs

| Input      | Default                                              | Description |
|------------|------------------------------------------------------|-------------|
| `excludes` | `.git .github .gitignore .DS_Store *.zip README.md`  | Space-separated blacklist of paths NOT part of the skill. Everything else in the repo root is packaged and synced. Override only to keep additional things out. |

### Secrets

`secrets: inherit` passes these through from the caller (set them as
**org-level secrets** scoped to the skill repos so they only need to exist once):

| Secret               | Description |
|----------------------|-------------|
| `SKILL_T_DEV_APP_ID` | GitHub App ID used to open cross-repo sync PRs. |
| `SKILL_T_DEV_KEY`    | GitHub App private key (PEM). |

The GitHub App must be installed on the three plugin repos with **Contents (write)**
and **Pull Requests (write)**.

## Requirements

- This repo's **Actions → General → Access** must allow use from other
  `temporalio` repositories (needed for internal/private reusable workflows).
- Callers pin to a tag (e.g. `@v1`). Advance the `v1` tag here to roll a fix
  out to every skill at once.
