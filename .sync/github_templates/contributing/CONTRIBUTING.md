# Contributing to Project Mu

Welcome, and thank you for your interest in contributing to Project Mu!

There are many ways in which you can contribute, beyond writing code. The goal of this document is to provide a
high-level overview of how you can get involved.

If this is your first time working with Project Mu, please keep in mind that many project details are maintained in
the [Project Mu Documentation](https://microsoft.github.io/mu/).

## Asking Questions

Have a question? Rather than opening an issue, please post your question under the `Q&A` category in the `Discussions`
section of the relevant Project Mu GitHub repo.

## Reporting Issues

Every Project Mu repo has an `Issues` section. Bug reports, feature requests, and documentation requests can all be
submitted in the issues section.

### Identify Where to Report

Project Mu is distributed across multiple repositories. Use features such as issues and discussions in the repository
most relevant to the topic.

Although we prefer items to be filed in the most relevant repo, if you're unsure which repo is most relevant, the item
can be filed in the [Project Mu Documentation Repo](https://github.com/microsoft/mu) and we will review the request and
move it to the relevant repo if necessary.

### Look For an Existing Issue

Before you create a new issue, please do a search in the issues section of the relevant repo to see if the issue or
feature request has already been filed.

If you find your issue already exists, make relevant comments and add your
[reaction](https://github.com/blog/2119-add-reactions-to-pull-requests-issues-and-comments). Use a reaction in place
of a "+1" comment:

* 👍 - upvote
* 👎 - downvote

If you cannot find an existing issue that describes your bug or feature, create a new issue using the guidelines below.

### Follow Your Issue

Please continue to follow your request after it is submitted to assist with any additional information that might be
requested.

### Pull Request Best Practices

Generally pull requests for UEFI code can become large and difficult to review due to the large number of build and
configuration files. To aid maintainers in reviewing your code we suggest adhering to the following guidelines:

1. Do keep code reviews single purpose; don't add more than one feature at a time.
2. Do fix bugs independently of adding features.
3. Do provide documentation and unit tests.
4. Do introduce code in digestable amounts; don't add more than 1000 lines per pull request.

As a general guide to help keep code digestable, you may consider breaking large pull requests into three smaller
pull requests the the general guide:

1. Interfaces (.h, .inf, documentation)
2. Implementatation (.c, unit-tests, unit-test build file); unit tests should build and run at this point
3. Integration/Build (.dec, .dsc, .fdf, integration tests); code added to platform and affects downstream consumers

By breaking the pull request into these three steps the reviewer can digest each piece independently, but each without
risk of breaking the main branch since without step 3 the code is shipping darkly (not directly integrated into the
build).

If any of these 3 pull requests is still larger than 1000 lines of code consider breaking the pull request down by the
following boundaries:

1. By .inf file; break each library/driver into its own 3 part pull request
2. By .c file; for large drivers break each .c file and its tests into a separate pull request

Feel free to create a draft pull request and ask for suggestions on how to split the pull request if you are unsure.

## Thank You

Thank you for your interest in Project Mu and taking the time to contribute!
