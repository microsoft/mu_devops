===================================================
Project Mu Developer Operations (DevOps) Repository
===================================================

|Latest Mu DevOps Release Version (latest SemVer)| |Commits Since Last Release| |Sync Mu DevOps Files to Mu Repos| |Containers Build|

.. |Latest Mu DevOps Release Version (latest SemVer)| image:: https://img.shields.io/github/v/release/microsoft/mu_devops?label=Latest%20Release
   :target: https://github.com/microsoft/mu_devops/releases/latest

.. |Commits Since Last Release| image:: https://img.shields.io/github/commits-since/microsoft/mu_devops/latest/main?include_prereleases
   :target: https://github.com/microsoft/mu_devops/releases

.. |Sync Mu DevOps Files to Mu Repos| image:: https://github.com/microsoft/mu_devops/actions/workflows/FileSyncer.yml/badge.svg
   :target: https://github.com/microsoft/mu_devops/actions/workflows/FileSyncer.yml

.. |Containers Build| image:: https://github.com/microsoft/mu_devops/actions/workflows/Build-Containers.yml/badge.svg?branch=main
   :target: https://github.com/microsoft/mu_devops/actions/workflows/Build-Containers.yml

This repository is part of Project Mu.  Please see Project Mu for details https://microsoft.github.io/mu

This repository is used to manage files related to build, continuous integration (CI), and continuous deployment (CD)
for other Project Mu repositories.

Many of these files are generic YAML templates that can be combined together to compose a fully functional pipeline.

Python based code leverages `edk2-pytools` to support cross platform building and execution.

You can find a high-level summary of the latest changes since the last release by viewing the `latest draft release`_.

.. _`latest draft release`: https://github.com/microsoft/mu_devops/releases

Table of Contents
=================

1. `Project Mu Developer Operations (DevOps) Repository`_

2. `Table of Contents`_

3. `Continuous Integration (CI)`_

   - `Code Coverage`_

4. `Conventions`_

5. `Containers`_

6. `GitHub Automation Workflow Overview`_

   - `Leaf Workflows & Reusable Workflows`_

   - `Reusable Workflows`_

   - `Leaf Workflows`_

7. `GitHub Automation Workflow Summary`_

   - `Auto Merge`_

   - `Auto Approver`_

   - `File Synchronization`_

   - `Initial Issue Triage`_

   - `Issue Assignment`_

   - `Label Automation`_

   - `Pull Request Validator`_

   - `Release Drafting`_

   - `Scheduled Maintenance`_

   - `Stale Detection`_

8. `GitHub Action Summary`_

   - `Submodule Release Updater`_

9. `Steps for Updating Rust Tool Chain`_

10.  `Links`_

Continuous Integration (CI)
===========================

There are two broad categories of CI - Core CI and Platform CI. You may see these terms used in the repo.
  - **Core CI** - Focused on building and testing all packages in Edk2 without an actual target platform.
  - **Platform CI** - Focused on building a single target platform and confirming functionality on that platform.

Code Coverage
-------------

mu_devops provides azure pipeline templates for uploading code coverage to the pipline currently executing, or directly
to codecov.io for public github repositories that use azure pipelines. No matter the yaml file you are using, whether
it be `MuDevOpsWrapper.yml`, `Jobs/PrGate.yml`, `Steps/PrGate.yml` or `Steps/UploadCodeCoverage.yml` itself, the only a
action that needs to be taken is to set an environment variable `coverage_upload_target` to ado or codecov.

Conventions
===========

- Shared templates in Project Mu repos are encouraged to be maintained in this repository.

- The `.github` directory contains GitHub collateral for this repository.

  - Some of the files are shared GitHub actions or workflows used (referenced) by other repositories as well.

- Files that are synced to other repositories should be placed in the `.sync` folder.

  - Some files are synced back to this repository (`mu_devops`).

- Azure Pipelines job and step templates should respectively be placed in the `Jobs` and `Steps` directories.

- YAML files should have the extensions `*.yml`.

  - An exception is the markdown configuration file (`.markdownlint.yaml`) that uses `.yaml` for consistency with
    pre-existing conventions across Mu repos.

Containers
==========

This repo maintains containers used throughout Project Mu projects. Containers provide well-defined, ready-to-go
images and result in improved performance, portability, and consistency of build environments. Project Mu leverages
containers for both server-side builds (e.g. pull requests and continuous integration) and for local developer builds.

At this time, containers are only offered for Linux. If you want to get started quickly and receive the smoothest
build experience, it is recommended to use containers where available.

The `Containers` directory contains the actual dockerfiles for building the containers. The containers are actually
built (in pull requests to dockerfiles and merges to the `main` branch) in the `.github/workflows/Build-Containers.yml`
workflow. On any change to a dockerfile a new container is built and pushed to the Microsoft GitHub container registry
as a container package associated with this repo. The latest Project Mu container builds are available in the
`Packages - Mu DevOps`_ container feed and more information is available in the `Container Readme file`_.

.. _`Container Readme file`: https://github.com/microsoft/mu_devops/blob/main/Containers/Readme.md
.. _`Packages - Mu DevOps`: https://github.com/orgs/microsoft/packages?repo_name=mu_devops

GitHub Automation Workflow Overview
===================================

This repository also drives automation of Project Mu GitHub repositories.

Leaf Workflows & Reusable Workflows
-----------------------------------

Workflows are split into two categories **(1) leaf** and **(2) reusable**.

The main reason for reusable workflows is to consolidate the main logic for the workflow to a single file and allow
the leaf workflow to be present in repositories that opt into what the reusable workflow provides. Leaf workflows can
provide any repo-specific input to a reusable workflow (if necessary). Leaf workflows can be considered minimal
wrappers around reusable workflows.

Reusable Workflows
------------------

These workflow are only designed to be called from other workflows. The files are maintained in the `.github/workflows`
directory of this repository. This is mandatory as GitHub only allows leaf workflows to call reusable workflows
located in this directory.

Review reusable workflow files to understand what they do and what input parameters are available.

Leaf Workflows
------------------

These workflow are only designed to call reusable workflows. They should not directly invoke GitHub Actions. The
actual GitHub Actions used by Project Mu are centrally tracked/updated in the single-copy reusable workflow files
in the Mu DevOps repo. This allows dependabot to update the actions here at once.

GitHub Automation Workflow Summary
==================================

Following is a brief summary of the actual workflows in the repository.

Auto Merge
----------

As automated bots pick up mundane tasks like syncing PIP module updates, submodules, files, and so on, an increasing
number of pull requests can accumulate that essentially update dependencies we expect to be updated over time. In most
cases, we simply care that the new update passes CI checks.

Therefore, Project Mu repos auto merge certain pull requests to reduce human burden of approving these requests in all
of the Project Mu repos. Individual repos can opt out of this functionality by removing the leaf workflow sync to their
repo, however, it is recommended to keep this flow enabled for consistency across all repos.

To see more about this flow look in these files:

- The main reusable workflow file:

  - `.github/workflows/AutoMerger.yml`

- The leaf workflow

  - `.sync/workflows/leaf/auto-merge.yml`

A Project Mu repo simply needs to sync `.sync/workflows/leaf/auto-merge.yml` to their repo in `Files.yml` and the
auto merge workflow will run in the repo.

Auto Approver
-------------

Auto approves pull requests from allowed bot accounts. As part of reducing dependency overhead, this workflow first
approves pull requests that are then auto merged after CI status checks complete. If a CI status check (e.g. build)
fails, the pull request will not be merged.

Note: This is currently disabled in most Project Mu repos.

To see more about this flow look in these files:

- The main reusable workflow file:

  - `.github/workflows/AutoApprover.yml`

- The leaf workflow

  - `.sync/workflows/leaf/auto-approve.yml`

A Project Mu repo simply needs to sync `.sync/workflows/leaf/auto-approve.yml` to their repo in `Files.yml` and the
auto approve workflow will run in the repo.

File Synchronization
--------------------

Because Project Mu is distributed over many repositories, a need arises to sync common files across all of the repos.
This is done via the `.github/workflows/FileSyncer.yml` workflow in Mu DevOps. It determines how to map files from
Mu DevOps to any repo with the configuration file `.sync/Files.yml`.

The configuration file can map any file in Mu DevOps to any file path in a destination repo. Flexibility is provided
to map the same file to different file paths in different repos, not map the file to some repos, etc. Whole directories
can also be synced as well.

The file sync operation automatically runs anytime a file in the `.sync/` directory of Mu DevOps is updated.

The file modification flow should be as follows:

1. Developer updates a synced file in Mu DevOps
2. Once PR for (1) is merged all mapped repos get a PR with the change
3. Reviewers in each repo review and approve the PR
4. The file is now in sync across all repos

File synchronization PRs are created by the `Project Mu UEFI Bot`_ account.

The file synchronization process will use the original commit title and message when syncing the change if it is
triggered on a single commit. Therefore, it is recommended to make changes to sync files one file per commit at a
time. If more than one file is modified, the PR is simply a single commit with a generic message containing both
changes.

.. _`Project Mu UEFI Bot`: https://github.com/uefibot

Initial Issue Triage
--------------------

This repo syncs `GitHub issue form templates`_ to many Project Mu repos. Part of initial triage for incoming issues
involves parsing data in the issue form to apply the appropriate labels so the issue is ready for triage by a human.

Issues need to be triaged by a human when the `state:needs-triage` label is present. This workflow can parse details
provided in issue forms to apply additional labels. For example, the `state:needs-owner` label is applied if the user
indicates they are not fixing the issue, the `urgency:<level>` label is applied based on user selection in the urgency
dropdown, etc.

A Project Mu repo simply needs to sync `.sync/workflows/leaf/triage-issues.yml` to their repo and the issue triage
workflow will run in the repo.

.. _`GitHub issue form templates`: https://github.com/microsoft/mu_devops/tree/main/.sync/github_templates/ISSUE_TEMPLATE

This workflow works in concert with other issue workflows such as `.sync/workflows/leaf/issue-assignment.yml` to
automate labels in issues based on the state of the issue.

Issue Assignment
----------------

A generic workflow that contains actions applied when GitHub issues are assigned. Currently, the workflow removes
labels from the issue that are no longer relevant after it is assigned.

To see more about this flow look in these files:

- The main reusable workflow file:

  - `.github/workflows/IssueAssignment.yml`

- The leaf workflow

  - `.sync/workflows/leaf/issue-assignment.yml`

Label Automation
----------------

Labels are automated from this repo in two main ways:

1. Automatically synchronize labels across all Project Mu repos
2. Automatically apply labels to issues and PRs

(1) is provided via the `.github/workflows/LabelSyncer.yml` reusable workflow with the labels defined in the file
`.github/Labels.yml`.

(2) is provided via the `.github/workflows/Labeler.yml` reusable workflow with the labeling configuration defined in
`.sync/workflows/config/label-issues`.

Labels are synced to all repos on a regular schedule that is the same for all repos.

Labels are automatically applied to issues and pull request on creation/modification and can be applied based on file
paths modified a pull request or content in the body of the issue or pull request.

Pull Request Validator
----------------------

Validates pull request formatting against requirements defined in the workflow. This workflow is not intended to
strictly validate exact formatting details but provide hints when simple, broad changes are needed to enhance the
quality of pull request verbiage.

- The leaf workflow

  - `.sync/workflows/leaf/pull-request-formatting-validator.yml`

Release Drafting
----------------

In order to ensure semantic versioning is followed based on well-defined labels used in Project Mu pull requests, the
release drafting process is automated. On every PR merge, a draft release is updated that contains the PR change entry
categorized according to the labels with the semantic version of the draft release updated according to the semantic
version specification.

This means, that the details for an upcoming release are always available, the release format is consistent across
Project Mu repos, and semantic versioning is followed consistently.

The draft release should be converted to an actual release any time the minor or major version is updated by a change.

To see more about this flow look in these files:

- The main reusable workflow file:

  - .github/workflows/ReleaseDrafter.yml

- The configuration file for the reusable workflow:

  - .sync/workflows/config/release-draft/release-draft-config.yml

    - This will be synced to .github/release-draft-config.yml in repos using release drafter

A Project Mu repo simply needs to sync `.sync/workflows/leaf/release-draft.yml` and the config file
`.sync/workflows/config/release-draft/release-draft-config.yml` to their repo and adjust any parameters needed in the
sync process (like repo default branch name) and the release draft workflow will run in the repo.

Scheduled Maintenance
---------------------

Performs regularly scheduled maintenance-related tasks such as closing pull requests and issues marked stale. Similar
tasks can be added to the workflow over time.

The leaf workflow contains the primary implementation and is directly synced to subscribed repos:

- `.sync/workflows/leaf/scheduled-maintenance.yml`

Stale Detection
---------------

Stale issues and pull requests are automatically labeled and closed after a configured amount of time.

This is provided by the `.github/workflows/Stale.yml` reusable workflow.

Individual repositories can control the label and time settings but it is strongly recommended to use the default
values defined in the reusable workflow for consistency.

GitHub Action Summary
=====================

Following is a brief summary of the GitHub Actions maintained in the repository.

Submodule Release Updater
-------------------------

A GitHub Action and leaf workflow that automatically create a pull request for any submodule in a repo
that has a new GitHub release available. The leaf workflow can easily be synced to repos and wraps around
the GitHub action.

- The GitHub action

  - `.github/actions/submodule-release-updater`

- The leaf workflow

  - `.sync/workflows/leaf/submodule-release-update.yml`

Steps for Updating Rust Tool Chain
=====================

Steps required to update the Rust tool chain in the Mu DevOps repo. The steps are as follows:

1. Update rust_toolchain in .sync/Version.njk to the new version. PR and merge to main.
2. Run Build Containers workflow to build a new linux container image (which will use updated .sync/Version.njk).
3. Update linux_build_container in .sync/Version.njk with the new version. PR and merge to main.
4. Create new mu_devops tag (GitHub release).
5. Update mu_devops in .sync/Version.njk to the newly generated tag. PR and merge to main.
6. Run Sync Mu DevOps Files to Mu Repos workflow to sync the new version to all Mu repos.
7. Complete associated PRs in the Mu repos.

Links
=====
- `Basic Azure Landing Site <https://docs.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops>`_
- `Pipeline jobs <https://docs.microsoft.com/en-us/azure/devops/pipelines/process/phases?view=azure-devops&tabs=yaml>`_
- `Pipeline YAML scheme <https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema?view=azure-devops&tabs=schema%2Cparameter-schema>`_
- `Pipeline Expressions <https://docs.microsoft.com/en-us/azure/devops/pipelines/process/expressions?view=azure-devops>`_
- `PyTool Extensions <https://github.com/tianocore/edk2-pytool-extensions>`_
- `PyTool Library <https://github.com/tianocore/edk2-pytool-library>`_
