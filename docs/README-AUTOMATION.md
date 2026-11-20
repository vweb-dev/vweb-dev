# VWEB.DEV Automatic Documentation System

## Objectives

**Public GitHub profile:** maintain an automatically refreshed index of all public original and upstream repositories under `vweb-dev`, excluding the profile repository and every private repository.

**Individual projects:** update a bounded, code-derived README snapshot on changes to the default branch. Preserve every handwritten README section, existing setup commands and caveats.

## Triggers and permissions

- The public directory runs every **six hours**, and via `workflow_dispatch`.
- Individual project READMEs run on source code pushes or manually via Actions.
- Each project gets a lightweight `.github/workflows/vweb-readme.yml` caller of the central reusable workflow.
- Each workflow uses its own repository's `GITHUB_TOKEN` with `contents: write` only. No shared personal access token.
- Workflow can be disabled by repo settings, policy, branch protection or Actions billing restrictions. Presence of a workflow file does **not** guarantee successful execution until a run completes.

## Scope

- Auto-generated panel: brand-neutral source-derived project title, available framework indicators, file types, top directories, code revision and SVG.
- The original README remains intact outside `<!-- VWEB:AUTO-README:START -->` / `END`.
- User-authored workflow descriptions, credentials, installation instructions and release notes are **not** auto-inferred or changed.
- Do not white-label third-party upstream forks. Template/empty repositories need individual review.
- Private repository data is never queried by the public profile workflow.
- Public repo directory is scheduled rather than instant; it may lag up to six hours.
- Auto-updates done with GitHub's `GITHUB_TOKEN` do not retrigger ordinary push workflows, preventing recursion. See GitHub Actions documentation.
- SVG motion uses CSS and includes reduced-motion media queries; rendering may vary by client.

## Install on any owned original project

Create `.github/workflows/vweb-readme.yml`:

```yaml
name: VWEB.DEV Auto README
on:
  push:
    paths-ignore:
      - README.md
      - assets/vweb-readme-banner.svg
      - .github/workflows/vweb-readme.yml
  workflow_dispatch:
permissions:
  contents: write
jobs:
  sync:
    if: ${{ github.ref == format('refs/heads/{0}', github.event.repository.default_branch) && !github.event.repository.fork }}
    uses: vweb-dev/vweb-dev/.github/workflows/reusable-readme.yml@main

```

Then run the workflow manually once, or push code to the default branch.

## Security and future upgrades

Keep source-sensitive files excluded; never store plaintext API keys or client credentials in READMEs. Prefer SHA-pinned reusable workflow references after initial QA. Avoid git pushes to protected branches without a reviewed PR.
