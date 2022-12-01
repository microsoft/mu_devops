===================================================
Project MU Developer Operations (DevOps) Repository
===================================================

|Latest Mu DevOps Release Version (latest SemVer)| |Sync Mu DevOps Files to Mu Repos|

.. |Sync Mu DevOps Files to Mu Repos| image:: https://github.com/microsoft/mu_devops/actions/workflows/FileSyncer.yml/badge.svg
   :target: https://github.com/microsoft/mu_devops/actions/workflows/FileSyncer.yml

.. |Latest Mu DevOps Release Version (latest SemVer)| image:: https://img.shields.io/github/v/release/microsoft/mu_devops?label=Latest%20Release
   :target: https://github.com/microsoft/mu_devops/releases/latest

This repository is part of Project Mu.  Please see Project Mu for details https://microsoft.github.io/mu

This repository is used to manage files related to build, continuous integration (CI), and continuous deployment (CD)
for other Project Mu repositories.

Many of these files are generic YAML templates that can be combined together to compose a fully functional pipeline.

Python based code leverages `edk2-pytools` to support cross platform building and execution.

Continuous Integration (CI)
===========================

There are two broad categories of CI - Core CI and Platform CI.
  - **Core CI** - Focused on building and testing all packages in Edk2 without an actual target platform.
  - **Platform CI** - Focused on building a single target platform and confirming functionality on that platform.

Conventions
===========

- Files extension should be `*.yml`. `*.yaml` is also supported but in edk2 we use those for our package
  configuration.
- Shared templates should be contributed to the `mu_devops` repository.
- Platform CI files should be placed in a `<PlatformPkg>/.azurepipelines` folder in the platform repository.
  - Top level CI files should be named `<HostOs><ToolChainTag>.yml`

GitHub Automation
=================

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

Stale Detection
---------------

Stale issues and pull requests are automatically labeled and closed after a configured amount of time.

This is provided by the `.github/workflows/Stale.yml` reusable workflow.

Individual repositories can control the label and time settings but it is strongly recommended to use the default
values defined in the reusable workflow for consistency.

Links
=====
- `Basic Azure Landing Site <https://docs.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops>`_
- `Pipeline jobs <https://docs.microsoft.com/en-us/azure/devops/pipelines/process/phases?view=azure-devops&tabs=yaml>`_
- `Pipeline YAML scheme <https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema?view=azure-devops&tabs=schema%2Cparameter-schema>`_
- `Pipeline Expressions <https://docs.microsoft.com/en-us/azure/devops/pipelines/process/expressions?view=azure-devops>`_
- `PyTool Extensions <https://github.com/tianocore/edk2-pytool-extensions>`_
- `PyTool Library <https://github.com/tianocore/edk2-pytool-library>`_
