# @file DownloadCargoBinaryFromGitHub.py
#
# A script used in pipelines to download Cargo binaries from a given GitHub
# repo.
#
# See the accompanying script readme for more details.
#
# The environment variables are (name and example value):
# - `BINARIES_DIR` - `$(Build.BinariesDirectory)`
# - `BINARY_NAME` - `cargo-make`
# - `DOWNLOAD_DIR` - `$(Build.ArtifactStagingDirectory)`
# - `REPO_URL` - `https://api.github.com/repos/sagiegurari/cargo-make/releases`
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause-Patent
##

import os
import requests
import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import Iterable

BINARY_NAME = os.environ["BINARY_NAME"]
REPO_URL = os.environ["REPO_URL"]
BINARIES_DIR = Path(os.environ["BINARIES_DIR"])
DOWNLOAD_DIR = Path(os.environ["DOWNLOAD_DIR"], "archives")

# Ensure the directories exist
BINARIES_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Fetch the list of assets from the GitHub releases
response = requests.get(REPO_URL)
response.raise_for_status()
releases = response.json()

if len(releases) == 0:
    print("Failed to find a release.")
    exit(1)

linux_found, windows_found = False, False

# Download assets
for release in releases:
    for asset in release['assets']:
        name = asset['name'].lower()
        if (("x86_64-pc-windows-msvc" in name or "x86_64-unknown-linux-gnu" in name)
        and asset['name'].endswith(('.zip', '.tar.gz', '.tgz'))):
            linux_found = linux_found or "x86_64-unknown-linux-gnu" in name
            windows_found = windows_found or "x86_64-pc-windows-msvc" in name
            filepath = DOWNLOAD_DIR / asset['name']
            print(f"Downloading {asset['name']}...")
            with requests.get(asset['browser_download_url'], stream=True) as r:
                with filepath.open('wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
    if linux_found and windows_found:
        break

# Extract files
for filename in DOWNLOAD_DIR.iterdir():
    extracted_dir = DOWNLOAD_DIR / filename.stem

    print(f"Extracting {filename.name}...")
    if filename.name.endswith('.zip'):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)
    elif filename.name.endswith(('.tar.gz', '.tgz')):
        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall(path=extracted_dir)

    def flatten_copy(src: Path, dst: Path, names: Iterable = ("",)):
        if not dst.exists():
            dst.mkdir(parents=True)

        for item in src.iterdir():
            print(f"item is {item}")
            if item.is_dir():
                flatten_copy(item, dst, names)
            elif any(name.lower() in item.name.lower() for name in names):
                shutil.copy2(item, dst)

    # Copy extracted files to the binaries directory
    flatten_copy(extracted_dir, BINARIES_DIR, (BINARY_NAME, "license"))
