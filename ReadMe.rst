===================================================
Project MU Developer Operations (DevOps) Repository
===================================================

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

Links
=====
- `Basic Azure Landing Site <https://docs.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops>`_
- `Pipeline jobs <https://docs.microsoft.com/en-us/azure/devops/pipelines/process/phases?view=azure-devops&tabs=yaml>`_
- `Pipeline YAML scheme <https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema?view=azure-devops&tabs=schema%2Cparameter-schema>`_
- `Pipeline Expressions <https://docs.microsoft.com/en-us/azure/devops/pipelines/process/expressions?view=azure-devops>`_
- `PyTool Extensions <https://github.com/tianocore/edk2-pytool-extensions>`_
- `PyTool Library <https://github.com/tianocore/edk2-pytool-library>`_
