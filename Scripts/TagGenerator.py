#
# Module for automatically tagging a commit with a release version.
#
# Copyright (c) Microsoft Corporation
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import argparse
import re
from git import Repo
from datetime import datetime
import time

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--repo", default=".",
                    help="Path to the repo directory.")
parser.add_argument("-b", "--base", type=str, required=True,
                    help="The base release version. This must be provided")
parser.add_argument("-f", "--format", default="BASE.MAJOR.MINOR",
                    help="The format of the release version. "
                    "Supported macros are BASE, MAJOR, and MINOR")
parser.add_argument("-n", "--notes", type=str,
                    help="Provides path to the release notes markdown file.")
parser.add_argument("--adovar", type=str,
                    help="An ADO variable to set to the tag name")
parser.add_argument("--notag", action="store_true",
                    help="Don't create the new tag")
parser.add_argument("--first", action="store_true",
                    help="Indicates this is expected to be the first tag.")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="Enabled verbose script prints.")

args = parser.parse_args()


def main():
    repo = Repo(args.repo)
    VerboseLog(f"Creating tag for: {repo.head.commit}")

    # Get the previous tag and increment values as needed.
    prev_tag, breaking, commits = GetLastTag(repo)

    # Generate the new tag name
    major = 0
    minor = 0
    if prev_tag is not None:
        if prev_tag.object.hexsha == repo.head.commit.hexsha:
            Log("No changes since last tag")
            return

        version_split = prev_tag.tag.split('.')
        if version_split[0] == args.base:
            major = int(version_split[1])
            minor = int(version_split[2])
            if breaking:
                major += 1
                minor = 0
            else:
                minor += 1
        else:
            VerboseLog(
                f"Different base version. {version_split[0]} -> {args.base}")

    version = f"{args.base}.{major}.{minor}"
    Log(f"New tag: {version}")
    if not args.notag:
        repo.create_tag(version, message=f"Release Tag {version}")

    if args.notes is not None:
        GenerateNotes(prev_tag.object.hexsha, version, commits)

    if args.adovar is not None:
        print(f"##vso[task.setvariable variable={args.adovar};]{version}")


def GetLastTag(repo):
    ref_log = repo.head.log()
    repo.tags
    breaking = False
    VerboseLog(f"{len(ref_log)} refs to check.")

    # TODO: This parsing is currently potentially broken if a commit has
    # multiple parents. Think on this.
    commit = repo.head.commit
    commits = []
    while commit is not None:
        if IsBreakingChange(commit.message):
            breaking = True

        VerboseLog(f"Checking commit {commit.hexsha}")
        for tag in repo.tags:
            if tag.commit.hexsha == commit.hexsha:
                Log(f"Previous tag: {tag} Breaking: {breaking}")
                return tag.tag, breaking, commits

        commits.append(commit)
        if commit.parents is None or len(commit.parents) == 0:
            break

        commit = commit.parents[0]

    if not args.first:
        raise ("No previous tag found!")

    Log("No previous tag found.")
    return None, breaking, commits


def GenerateNotes(commit_hash, version, commits):
    notes_file = open(args.notes, 'r+')
    old_lines = notes_file.readlines()
    notes_file.seek(0)

    # Collect all the notable changes
    breaking_changes = []
    security_changes = []
    features = []
    other_changes = []
    contributors = []

    for commit in commits:
        if commit.author not in contributors:
            contributors.append(commit.author)

        if IsBreakingChange(commit.message):
            breaking_changes.append(commit)
        elif IsSecurityChange(commit.message):
            security_changes.append[commit]
        elif IsNewFeature(commit.message):
            features.append(commit)
        else:
            other_changes.append(commit)

    timestamp = time.strftime("%a, %D %T", time.gmtime())
    notes = f"\n# Release {version}\n\n"
    notes += f"Created {timestamp} GMT\n\n"
    notes += f"{len(commits)} commits. {len(contributors)} contributors.\n"

    if len(breaking_changes) > 0:
        notes += f"\n## Breaking Changes\n\n"
        notes += GetChangeList(breaking_changes)

    if len(security_changes) > 0:
        notes += f"\n## Security Changes\n\n"
        notes += GetChangeList(security_changes)

    if len(other_changes) > 0:
        notes += f"\n## Changes\n\n"
        notes += GetChangeList(other_changes)

    notes += "\n## Contributors\n\n"
    for contributor in contributors:
        notes += f"- {contributor.name} \<{contributor.email}\>"

    # Add new notes at the top and write out existing content.
    notes_file.write(notes)
    for line in old_lines:
        notes_file.write(line)


def GetChangeList(commits):
    changes = ""
    for commit in commits:
        msg = commit.message.split('\n', 1)[0]
        changes += f"- {msg} -- {commit.author}\n"

    return changes


def IsBreakingChange(message):
    return re.search('\[x\] breaking change', message, flags=re.IGNORECASE) is not None


def IsSecurityChange(message):
    return re.search('\[x\] fixes security issue', message, flags=re.IGNORECASE) is not None


def IsNewFeature(message):
    return re.search('\[x\] new feature', message, flags=re.IGNORECASE) is not None


def Log(string):
    print(string)


def VerboseLog(string):
    if args.verbose:
        print(string)


main()
