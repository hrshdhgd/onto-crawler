# -*- coding: utf-8 -*-
"""Onto-crawl API section."""
import re
from os.path import join
from pathlib import Path
from typing import Generator, Optional

from github import Github

# Token.txt unique to every user.
# For more information:
#   https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
# Save the token in a txt file as named below.
SRC = Path(__file__).parent
TOKEN_FILE = join(SRC, "token.txt")

with open(TOKEN_FILE, "r") as t:
    TOKEN = t.read().rstrip()

g = Github(TOKEN)
# Example for API: https://pygithub.readthedocs.io/en/latest/examples.html


def get_issues(
    repository_name: str,
    title_search: Optional[str] = None,
    label: Optional[str] = None,
    number: Optional[int] = 0,
    state: str = "open",
) -> Generator:
    """Get issues of specific states from a Github repository.

    :param repository_name: Name of the repository [org/repo]
    :param title_search: Regex for title of the issue.
    :param state: State of the issue e.g. open, close etc., defaults to "open"
    :yield: Issue names that match the regex.
    """
    repo = g.get_repo(repository_name)
    label_object = None
    if label:
        label_object = repo.get_label(label)

    issues = repo.get_issues(state=state)

    for issue in issues:
        if title_search is None and label_object is None and number == 0:
            yield issue
        else:
            if title_search and re.match(title_search, issue.title):
                yield issue
            if label_object and label_object in issue.labels:
                yield issue
            if number and number == issue.number:
                yield issue


def get_all_labels_from_repo(repository_name: str) -> dict:
    """Get all labels available in a repository for tagging issues on creation.

    :param repository_name: Name of the repository.
    :return: A dictionary of {name: description}
    """
    repo = g.get_repo(repository_name)
    return {label.name: label.description for label in repo.get_labels()}
