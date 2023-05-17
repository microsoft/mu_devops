# MU Devops Containers

Project MU uses containers to build on Linux. These containers come with all of
the tools expected for CI and virtual platform pipelines and local development.
Containers can be pulled. For more details see the [mu_devops packages page](https://github.com/orgs/microsoft/packages?repo_name=mu_devops).

## Container Images

### Ubuntu-22 _(Recommended)_

[![Ubuntu 22 Containers](https://github.com/microsoft/mu_devops/actions/workflows/Container-Ubuntu-22.yml/badge.svg?branch=main)](https://github.com/microsoft/mu_devops/actions/workflows/Container-Ubuntu-22.yml)

The MU Ubuntu container provides the following layers.

| Name  | Description                          | Package |
|-------|--------------------------------------|---------|
| Build | Used for CI pipeline builds.         | [ubuntu-22-build](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-22-build) |
| Test  | Used for virtual platform pipelines. | [ubuntu-22-test](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-22-test) |
| Dev   | Used local development.              | [ubuntu-22-dev](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-22-dev) |
