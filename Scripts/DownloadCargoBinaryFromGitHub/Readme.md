# Download Cargo Binary From GitHub Script

[DownloadCargoBinaryFromGitHub.py](./DownloadCargoBinaryFromGitHub.py) is a script used in pipelines to download Cargo
binaries from a given GitHub repo.

## Responsibilities

The script manages:

- Downloading the binary onto the agent
- Extracting relevant binaries
  - Currently Windows and Linux GNU x86_64 binaries
- Placing the binaries in the given binaries directory

## Background

This is intended to provide more fine grained control over the process (as opposed to built-in GitHub release download
tasks), to optimize file filtering, and accommodate future adjustments such as expanding support for additional file
checks or archive formats, etc. while also being portable between CI environments. For example, it can be directly
reused between Azure Pipelines and GitHub workflows without swapping out tasks, changing service connection details,
and so on while also encasing operations like file extraction.

## Inputs

Because this script is only intended to run in pipelines, it does not present a user-facing command-line parameter
interface and accepts its input as environment variables that are expected to be passed in the environment variable
section of the task that invokes the script.

The environment variables are (name and example value):

- `BINARIES_DIR` - `$(Build.BinariesDirectory)`
- `BINARY_NAME` - `cargo-make`
- `DOWNLOAD_DIR` - `$(Build.ArtifactStagingDirectory)`
- `REPO_URL` - `https://api.github.com/repos/sagiegurari/cargo-make/releases`
