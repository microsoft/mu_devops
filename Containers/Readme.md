# Mu Devops Containers

Project Mu uses containers to build on Linux. These containers come with all of
the tools expected for CI and virtual platform pipelines and local development.
Containers can be pulled. For more details see the [mu_devops packages page](https://github.com/orgs/microsoft/packages?repo_name=mu_devops).

## Ubuntu-24 _(Recommended)_

The Mu Ubuntu container provides the following layers. Ubuntu-24 is the recommended
container image because it best aligns with existing development flows and provides
tools needed to cross compile both kernel and user mode components needed in Mu.

## Ubuntu-22

Ubuntu-22 is the previous Ubuntu container image used in Mu CI from May 2023 until
February 2025. It is still available for use, but is not recommended for new projects
and other CI dependencies and worfklows may not be supported with it.

It will be deprecated soon. Users should migrate to Ubuntu-24 as soon as possible.

---

| Name  | Description                          | Package |
|-------|--------------------------------------|---------|
| Build | Used for CI pipeline builds.         | [ubuntu-24-build](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-24-build) |
| Test  | Used for virtual platform pipelines. | [ubuntu-24-test](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-24-test) |
| Dev   | Used local development.              | [ubuntu-24-dev](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-24-dev) |
| Build | Ubuntu 22 (older) pipeline build.    | [ubuntu-22-build](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-22-build) |
| Test  | Ubuntu 22 (older) virt plat image.   | [ubuntu-22-test](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-22-test) |
| Dev   | Ubuntu 22 (older) local dev image    | [ubuntu-22-dev](https://github.com/microsoft/mu_devops/pkgs/container/mu_devops%2Fubuntu-22-dev) |
