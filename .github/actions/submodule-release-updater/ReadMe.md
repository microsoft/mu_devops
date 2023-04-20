# Project Mu Submodule Release Updater GitHub Action

This GitHub Action checks if new releases are available for submodules and creates pull requests to update
them. A single pull request is opened per submodule. At this time, the action should only be used within
Project Mu repositories.

## How to Use

1. Create a GitHub workflow in a repository
2. Add this GitHub Action as a step to the workflow
3. Configure the workflow to trigger as desired
   - It is recommended to trigger the workflow on a schedule (e.g. daily) to check for new releases.

### Example Workflow

```yaml
name: Update Submodules to Latest Release

on:
  schedule:
    - cron: '0 0 * * MON'  # https://crontab.guru/every-monday

jobs:
  repo_submodule_update:
    name: Check for Submodule Releases
    runs-on: ubuntu-latest

    steps:
      - name: Update Submodules to Latest Release
        uses: microsoft/mu_devops/.github/actions/submodule-release-updater@v2.4.0
        with:
          GH_PAT: ${{ secrets.SUBMODULE_UPDATER_TOKEN }}
          GH_USER: "Add GitHub account username here"
          GIT_EMAIL: "Add email address here"
          GIT_NAME: "Add git author name here"

```

## Action Inputs

- `GH_PAT` - **Required** - GitHub Personal Access Token (PAT) with `repo` scope
- `GH_USER` - **Required** - GitHub username
- `GIT_EMAIL` - **Required** - Email address to use for git commits
- `GIT_NAME` - **Required** - Name to use for git commits

## Action Outputs

- `submodule-update-count` - Number of submodules updated. `0` if no submodules were updated.

## Limitations

- This action is only intended to work within Project Mu repositories.
- This action only supports repositories hosted on GitHub.
- This action only updates submodules that are hosted on GitHub.
- This action is only intended to work with submodules that use [semantic versioning](https://semver.org/).
- Submodules should already be set to a specific release before enabling this action.
  - This allows the action to compare new versions to the current version.
- This action does not automatically close stale PRs when a new release is available.
