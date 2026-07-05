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
    inputs:
      bump:
        description: "Version bump for a one-click release"
        type: choice
        required: true
        default: patch
        options: [patch, minor, major]

jobs:
  package-and-sync:
    uses: temporalio/skill-ci/.github/workflows/package-and-sync.yml@v1
    permissions:
      contents: write
    secrets: inherit
    with:
      # On workflow_dispatch this is the chosen bump; on push it's empty.
      bump: ${{ inputs.bump }}
      # includes: "SKILL.md agents references scripts"
```

That's the entire caller. The reusable workflow derives the skill name from the
caller repo's name (dropping the `skill-` prefix) and opens sync PRs against the
plugin repos. There are two ways to cut a release:

- **One-click (recommended):** run the workflow manually (Actions → *Run
  workflow*) and pick a `bump` (`patch`/`minor`/`major`). The workflow rewrites
  `version:` in `SKILL.md`, pushes that commit to `main`, then releases + syncs.
- **Manual edit:** bump `version:` in `SKILL.md` yourself and push to `main`; the
  workflow releases + syncs when it sees a version it hasn't tagged yet.

### Inputs

| Input      | Default                              | Description |
|------------|--------------------------------------|-------------|
| `includes` | `SKILL.md agents references scripts` | Space-separated whitelist of paths that ARE part of the skill. Only these are packaged and synced; everything else is ignored. Missing entries are skipped, so the default can list optional dirs. Override to add new skill content. |
| `bump`     | `""` (empty)                         | One-click release: `patch`, `minor`, or `major`. When set, rewrites `SKILL.md`'s version and pushes the bump to the default branch before releasing. Empty (push events) => release only on a manual version change. Requires `RELEASE_SSH_KEY`. |

### Secrets

`secrets: inherit` passes these through from the caller (set them as
**org-level secrets** scoped to the skill repos so they only need to exist once):

| Secret               | Required | Description |
|----------------------|----------|-------------|
| `SKILL_T_DEV_APP_ID` | yes      | GitHub App ID used to open cross-repo sync PRs. |
| `SKILL_T_DEV_KEY`    | yes      | GitHub App private key (PEM). |
| `RELEASE_SSH_KEY`    | for `bump` | SSH deploy key used to push the version-bump commit to the default branch. Only needed if you use the one-click `bump`. |

The GitHub App must be installed on the three plugin repos with **Contents (write)**
and **Pull Requests (write)**.

`RELEASE_SSH_KEY` is a **per-repo** deploy key (each skill repo needs its own key
pair — set the private key as a repo secret, add the public key as a deploy key
with write access). Because pushes to `main` are ruleset-protected, the deploy key
must also be listed in the default branch ruleset's **bypass actors**.

## Requirements

- This repo's **Actions → General → Access** must allow use from other
  `temporalio` repositories (needed for internal/private reusable workflows).
- Callers pin to a tag (e.g. `@v1`). Advance the `v1` tag here to roll a fix
  out to every skill at once.
