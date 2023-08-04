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
parser.add_argument("-n", "--notes", type=str,
                    help="Provides path to the release notes markdown file.")
parser.add_argument("--tagvar", type=str,
                    help="An ADO variable to set to the tag name")
parser.add_argument("--url", type=str, default="",
                    help="The URL to the repo, used for tag notes.")
parser.add_argument("--create", action="store_true",
                    help="Create the new tag")
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
        if prev_tag.commit == repo.head.commit:
            Log("No changes since last tag")
            return

        version_split = prev_tag.name.split('.')
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

    # Before going further, ensure this is not a duplicate. This can happen if
    # there are tags detached from their intended branch.
    for tag in repo.tags:
        if tag.name == version:
            raise Exception(
                "Duplicate tag! Check for tags not in branch history.")

    if args.create:
        repo.create_tag(version, message=f"Release Tag {version}")

    if args.notes is not None:
        GenerateNotes(version, commits)

    if args.tagvar is not None:
        print(f"##vso[task.setvariable variable={args.tagvar};]{version}")


def GetLastTag(repo):
    breaking = False
    included_commits = []
    commits = repo.iter_commits(repo.head.commit)

    # Find all the eligible tags first.
    tags = []
    pattern = re.compile("^[0-9]+\.[0-9]+\.[0-9]+$")
    for tag in repo.tags:
        if pattern.match(tag.name) is None:
            VerboseLog(f"Skipping unrecognized tag format. Tag: {tag}")
            continue

        tags.append(tag)

    # Find the most recent commit with a tag.
    for commit in commits:
        if IsBreakingChange(commit.message):
            breaking = True

        VerboseLog(f"Checking commit {commit.hexsha}")
        for tag in tags:
            if tag.commit == commit:
                Log(f"Previous tag: {tag} Breaking: {breaking}")
                return tag, breaking, included_commits

        included_commits.append(commit)

    if not args.first:
        raise Exception("No previous tag found!")

    # No tag found, return all commits and non-breaking.
    Log("No previous tag found.")
    return None, False, commits


def GenerateNotes(version, commits):
    notes_file = open(args.notes, 'a+')
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
        notes += f"- {contributor.name} <<{contributor.email}>>"

    notes += "\n"

    # Add new notes at the top and write out existing content.
    notes_file.write(notes)
    for line in old_lines:
        notes_file.write(line)


def GetChangeList(commits):
    changes = ""

    for commit in commits:
        pr = None
        msg = commit.message.split('\n', 1)[0]
        match = re.match('Merged PR [0-9]+:', msg, flags=re.IGNORECASE)
        if match:
            pr = msg[len("Merged PR "):match.end() - 1]
            msg = f"[{msg[0:match.end()]}]({args.url}/pullrequest/{pr}){msg[match.end():]}"

        changes += f"- {msg} ~ _{commit.author}_\n"

    return changes


def IsBreakingChange(message):
    return re.search('\[x\] breaking change', message, flags=re.IGNORECASE) is not None


def IsSecurityChange(message):
    return re.search('\[x\] security fix', message, flags=re.IGNORECASE) is not None


def IsNewFeature(message):
    return re.search('\[x\] new feature', message, flags=re.IGNORECASE) is not None


def Log(string):
    print(string)


def VerboseLog(string):
    if args.verbose:
        print(string)


main()
