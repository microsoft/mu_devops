===============================
Project Mu File Synchronization
===============================

This directory contains files that are synchronized to Project Mu repositories.

::

  Note: Any files that are not synchronized should not be added in this directory.

Why?
----

- To automatically keep all repos up-to-date.
- To ensure consistency of file content across repos.
- To centralize content for files that need to be local to a repo (e.g. a GitHub action) but contain the same content
  across more than one Project Mu repo.
- To minimize developer time to push file changes across repos.

When?
-----

- Anytime a file in this directory (`/.sync`_) is updated
- Anytime the workflow that synchronizes files is updated (`/.github/workflows/FileSyncer.yml`_)
- `Manually`_

.. _/.github/workflows/FileSyncer.yml: https://github.com/microsoft/mu_devops/blob/main/.github/workflows/FileSyncer.yml
.. _/.sync: https://github.com/microsoft/mu_devops/blob/main/.sync/
.. _Manually: https://github.com/microsoft/mu_devops/actions/workflows/FileSyncer.yml

How to Configure File Syncing
-----------------------------

All of the file synchronization settings are maintained in the `/.sync/Files.yml`_ configuration file. Refer to the file
to see the current synchronization settings and to modify settings.

.. _/.sync/Files.yml: https://github.com/microsoft/mu_devops/blob/main/.sync/Files.yml
