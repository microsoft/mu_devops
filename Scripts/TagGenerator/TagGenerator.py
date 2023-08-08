#
# Module for automatically tagging a commit with a release version.
#
# Copyright (c) Microsoft Corporation
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import argparse
import re
import time
import logging
from git import Repo


def main():
    """Main entry point for the TagGenerator script"""

    args = get_cli_options()
    repo = Repo(args.repo)
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format="%(levelname)s - %(message)s", level=log_level)

    logging.debug(f"Generating tag name for: {repo.head.commit}")

    # Get the previous tag and increment values as needed.
    prev_tag, breaking, commits = get_last_tag(repo, args.first)

    # Generate the new tag name
    minor = 0
    patch = 0
    if prev_tag is not None:
        if prev_tag.commit == repo.head.commit:
            logging.info("No changes since last tag")
            return

        version_split = prev_tag.name.split('.')
        if version_split[0] == args.major:
            minor = int(version_split[1])
            patch = int(version_split[2])
            if breaking:
                minor += 1
                patch = 0
            else:
                patch += 1
        else:
            logging.critical(
                f"Different major version. {version_split[0]} -> {args.major}")
            if int(version_split[0]) > int(args.major):
                raise Exception("Major version has decreased!")

    version = f"{args.major}.{minor}.{patch}"
    logging.info(f"New tag: {version}")

    # Before going further, ensure this is not a duplicate. This can happen if
    # there are tags detached from their intended branch.
    for tag in repo.tags:
        if tag.name == version:
            raise Exception(
                "The new tag name already exists! Check tags already present in the repo.")

    if args.create:
        repo.create_tag(version, message=f"Release Tag {version}")

    if args.notes is not None:
        generate_notes(version, commits, args.notes, args.url)

    if args.printadovar is not None:
        print(f"##vso[task.setvariable variable={args.printadovar};]{version}")


def get_cli_options():
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--repo", default=".",
                        help="Path to the repo directory.")
    parser.add_argument("-m", "--major", type=str, required=True,
                        help="The major release version. This must be provided")
    parser.add_argument("-n", "--notes", type=str,
                        help="Provides path to the release notes markdown file.")
    parser.add_argument("--printadovar", type=str,
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
    return args


def get_last_tag(repo, first):
    """Retrieves the last tag name in the given HEAD history. This will
    exclude any tag that does not match the #.#.# format.

    repo - Provides the Git Repo object which will be searched.
    first - Indicates this may be the first tag generation run.
    """

    breaking = False
    included_commits = []
    commits = repo.iter_commits(repo.head.commit)

    # Find all the eligible tags first.
    tags = []
    pattern = re.compile("^[0-9]+\.[0-9]+\.[0-9]+$")
    for tag in repo.tags:
        if pattern.match(tag.name) is None:
            logging.debug(f"Skipping unrecognized tag format. Tag: {tag}")
            continue

        tags.append(tag)

    # Find the most recent commit with a tag.
    for commit in commits:
        if is_breaking_change(commit.message):
            breaking = True

        logging.debug(f"Checking commit {commit.hexsha}")
        for tag in tags:
            if tag.commit == commit:
                logging.info(f"Previous tag: {tag} Breaking: {breaking}")
                return tag, breaking, included_commits

        included_commits.append(commit)

    if not first:
        raise Exception("No previous tag found!")

    # No tag found, return all commits and non-breaking.
    logging.info("No previous tag found.")
    return None, False, commits


def generate_notes(version, commits, filepath, url):
    """Generates notes for the provided tag version including the provided commit
    list. These notes will include the list of Breaking, Security, and other
    commits. These notes will be prepended to the file specify by filepath

    version - The tag version string.
    commits - The list of commits since the last tag.
    filepath - The path to the file to prepend the notes to.
    url - The URL of the repository.
    """

    notes_file = open(filepath, 'a+')
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

        if is_breaking_change(commit.message):
            breaking_changes.append(commit)
        elif is_security_change(commit.message):
            security_changes.append[commit]
        elif is_new_feature(commit.message):
            features.append(commit)
        else:
            other_changes.append(commit)

    timestamp = time.strftime("%a, %D %T", time.gmtime())
    notes = f"\n# Release {version}\n\n"
    notes += f"Created {timestamp} GMT\n\n"
    notes += f"{len(commits)} commits. {len(contributors)} contributors.\n"

    if len(breaking_changes) > 0:
        notes += f"\n## Breaking Changes\n\n"
        notes += get_change_list(breaking_changes, url)

    if len(security_changes) > 0:
        notes += f"\n## Security Changes\n\n"
        notes += get_change_list(security_changes, url)

    if len(features) > 0:
        notes += f"\n## New Features\n\n"
        notes += get_change_list(features, url)

    if len(other_changes) > 0:
        notes += f"\n## Changes\n\n"
        notes += get_change_list(other_changes, url)

    notes += "\n## Contributors\n\n"
    for contributor in contributors:
        notes += f"- {contributor.name} <<{contributor.email}>>"

    notes += "\n"

    # Add new notes at the top and write out existing content.
    notes_file.write(notes)
    for line in old_lines:
        notes_file.write(line)


def get_change_list(commits, url):
    """Generates a list of changes for the given commits. The routine will attempt
    to create links to the appropriate ADO pages from the URL script argument where
    applicable.

    commits - The list of commits which to create the list for
    url - The URL of the repository.
    """

    changes = ""

    for commit in commits:
        pr = None
        msg = commit.message.split('\n', 1)[0]
        match = re.match('Merged PR [0-9]+:', msg, flags=re.IGNORECASE)
        if match:
            pr = msg[len("Merged PR "):match.end() - 1]
            msg = f"[{msg[0:match.end()]}]({url}/pullrequest/{pr}){msg[match.end():]}"

        changes += f"- {msg} ~ _{commit.author}_\n"

    return changes


def is_breaking_change(message):
    """Checks if the given commit message contains the breaking change tag"""
    return re.search('\[x\] breaking change', message, flags=re.IGNORECASE) is not None


def is_security_change(message):
    """Checks if the given commit message contains the security change tag"""
    return re.search('\[x\] security fix', message, flags=re.IGNORECASE) is not None


def is_new_feature(message):
    """Checks if the given commit message contains the new feature tag"""
    return re.search('\[x\] new feature', message, flags=re.IGNORECASE) is not None


if __name__ == '__main__':
    main()
