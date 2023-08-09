# Tag Generator Script

[TagGenerator.py](./TagGenerator.py) will automatically generate the next version tag
and add notes to a release notes file for the current git HEAD. The Tag Generator
script is primarily intended for use by the [Generate Tag Pipeline](../../Jobs/GenerateTag.yml)
but can be used locally as well. This script is intended to be used for ADO repositories,
but may be used for GitHub, though certain features may not work in their current
form such as PR links in tag notes.

## Versioning Scheme

This script uses the `major.minor.patch` versioning scheme, but diverges from semantic
versioning in some significant ways.

- `major version` - Indicates the EDKII release tag that the repo is compiled against, e.g. `202302`.
- `minor version` - Indicates the breaking change number since the last major version change.
- `patch version` - Indicates the number of non-breaking changes since the last minor version.

## Repro Requirements

For this script to work properly it makes assumptions about the repository and
project structure for tag history and generating notes.

### Pull Request Template

To determine what kind of change each commit is, this script expects certain strings
exists in the commit message. It is recommended consumers include these in the PR
templates for the repository. The script expects `[x] Breaking Change` for breaking
changes, `[x] Security Fix` for security changes, and `[x] New Feature` for new
features. The template forms of these are provided below.

```md
- [ ] Breaking Change
- [ ] Security Fix
- [ ] New Feature
```
