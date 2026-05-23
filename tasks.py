import os
import tomllib
from pathlib import Path

from colorama import Fore, init
from invoke import task


def create_release(c, branch, is_first_release=False, push=False):
    """Create a release by combining `commitizen-tools` and `commit-and-tag-version`

    commitizen-tools understands Python stuff, but I don't like the
    generated changelogs. I decided to use commit-and-tag-version instead.
    Unfortunately, commit-and-tag-version doesn't understand Python projects,
    so I make the two work together.

    This requires `commit-and-tag-version` to be installed on your machine:
    ``npm i -g commit-and-tag-version``

    See <https://github.com/absolute-version/commit-and-tag-version> for more details.

    The logic here is as follows:

    1. cz bump --files-only
    2. git add pyproject.toml and other files specified in pyproject.toml
    3. commit-and-tag-version --commit-all --release-as <result from cz if not none>
    4. git push --follow-tags origin [branch]
    """
    if is_first_release:
        print(f"{Fore.YELLOW}Generating changelog for first release ...{Fore.RESET}")
        c.run(
            'commit-and-tag-version --first-release --releaseCommitMessageFormat "chore: first release v{{{{currentTag}}}} 🎉"',
            pty=True,
        )
        if push:
            c.run(f"git push --follow-tags origin {branch}", pty=True)
    else:
        print(f"{Fore.MAGENTA}Attempting to bump using commitizen-tools ...{Fore.RESET}")
        c.run("cz bump --files-only > .bump_result.txt", pty=True)
        str_of_interest = "increment detected: "
        result = ""
        with open(".bump_result.txt") as br:
            for line in br:
                if str_of_interest in line:
                    result = line
                    break
        release_type = result.replace(str_of_interest, "").strip("\n").lower()
        print(f"cz bump result: {release_type}")
        if release_type == "none":
            print(f"{Fore.YELLOW}No increment detected, cannot bump{Fore.RESET}")
        elif release_type in ["major", "minor", "patch"]:
            print(f"{Fore.GREEN}Looks like the bump command worked!{Fore.RESET}")
            print(f"{Fore.GREEN}Now handing over to commit-and-tag-version ...{Fore.RESET}")
            with open("pyproject.toml", "rb") as f:
                toml_dict = tomllib.load(f)
            version_files = toml_dict["tool"]["commitizen"]["version_files"]
            files_to_add = " ".join(version_files)
            c.run(f"git add pyproject.toml {files_to_add}", pty=True)
            print(f"{Fore.GREEN}let me retrieve the tag we're bumping from ...{Fore.RESET}")
            get_current_tag = c.run(
                "git describe --abbrev=0 --tags `git rev-list --tags --skip=0  --max-count=1`",
                pty=True,
            )
            previous_tag = get_current_tag.stdout.rstrip()
            c.run(
                f'commit-and-tag-version --commit-all --release-as {release_type} --releaseCommitMessageFormat "bump: ✈️ {previous_tag} → v{{{{currentTag}}}}"',
                pty=True,
            )
            if push:
                c.run(f"git push --follow-tags origin {branch}", pty=True)
        else:
            print(f"{Fore.RED}Something went horribly wrong, please investigate & fix it!{Fore.RESET}")
            print(f"{Fore.RED}Bump failed!{Fore.RESET}")

        Path(".bump_result.txt").unlink(missing_ok=True)


@task(
    help={
        "version": "show program's version number and exit",
        "plain": "Plain colour mode. Standard green badge",
        "help": "show this help message and exit",
    }
)
def run(c, version=False, plain=False, help=False):
    """run the program"""

    if version:
        c.run("python readme_coverage_badger/__main__.py -v", pty=True)
    elif plain:
        c.run("python readme_coverage_badger/__main__.py -p", pty=True)
    elif help:
        c.run("python readme_coverage_badger/__main__.py -h", pty=True)
    else:
        c.run("python readme_coverage_badger/__main__.py", pty=True)


@task
def test(c):
    """run tests"""
    c.run("pytest", pty=True)


@task(help={"fix": "let black and isort format your files"})
def lint(c, fix=False):
    """flake8, black, isort and mypy"""

    if fix:
        c.run("black .", pty=True)
        c.run("isort --profile black .", pty=True)
    else:
        c.run("mypy readme_coverage_badger", pty=True)
        c.run("black . --check", pty=True)
        c.run("isort --check-only --profile black .", pty=True)
        c.run("flake8 tests readme_coverage_badger", pty=True)


# TODO: create a "clean" collection comprising the next three tasks below


@task
def clean_build(c):
    """remove build artifacts"""

    # TODO: Make this more portable, as it'll probably break on a Windows prompt
    c.run("rm -fr build/", pty=True)
    c.run("rm -fr dist/", pty=True)
    c.run("rm -fr .eggs/", pty=True)
    c.run("find . -name '*.egg-info' -exec rm -fr {} +", pty=True)
    c.run("find . -name '*.egg' -exec rm -f {} +", pty=True)


@task
def clean_pyc(c):
    """remove Python file artifacts"""

    # TODO: Make this more portable, as it'll probably break on a Win32 prompt
    c.run("find . -name '*.pyc' -exec rm -f {} +", pty=True)
    c.run("find . -name '*.pyo' -exec rm -f {} +", pty=True)
    c.run("find . -name '*~' -exec rm -f {} +", pty=True)
    c.run("find . -name '__pycache__' -exec rm -fr {} +", pty=True)


@task
def clean_test(c):
    """remove test and coverage artifacts"""

    # TODO: Make this more portable, as it'll probably break on a Win32 prompt
    c.run("rm -fr .tox/", pty=True)
    c.run("rm -f .coverage", pty=True)
    c.run("rm -f coverage.xml", pty=True)
    c.run("rm -fr htmlcov/", pty=True)
    c.run("rm -fr .pytest_cache", pty=True)


@task(
    help={
        "branch": "The branch against which you wanna bump (default: master)",
        "first": "Is this the first release?",
    }
)
def bump(c, branch="master", first=False):
    """Use Commitizen Tools & commit-and-tag-version to bump version and generate changelog

    Run this task when you want to prepare a release.
    First we check that there are no unstaged files before running
    """

    init()

    unstaged_str = "not staged for commit"
    uncommitted_str = "to be committed"
    check = c.run("git status", pty=True)
    if unstaged_str not in check.stdout or uncommitted_str not in check.stdout:
        create_release(c, branch, first, push=False)
    else:
        print(f"{Fore.RED}Sorry mate, please ensure there are no unstaged files before creating a release{Fore.RESET}")


@task
def dist(c):
    """builds source and wheel package"""

    # TODO: provide a "clean" option, and improve portability
    c.run("python -m build", pty=True)
    c.run("ls -lah dist", pty=True)
    c.run("pwd", pty=True)


@task
def release(c):
    """(package and) upload an official release"""

    # TODO: provide a "dist" option, so that we build first then release
    c.run("twine upload dist/*", pty=True)


@task
def release_testpypi(c):
    """(package and) upload a test release on https://test.pypi.org/"""

    # TODO: provide a "dist" option, so that we build first then release
    c.run("twine upload -r testpypi dist/*", pty=True)


@task
def get_release_notes(c):
    """extract content from CHANGELOG.md for use in Github Releases

    we read the file and loop through line by line
    we wanna extract content beginning from the first Heading 2 text
    to the last line before the next Heading 2 text
    """

    pattern_to_match = "## [v"

    count = 0
    lines = []
    heading_text = "## What's changed in this release\n"
    lines.append(heading_text)

    with open("CHANGELOG.md", "r") as c:
        for line in c:
            if pattern_to_match in line and count == 0:
                count += 1
            elif pattern_to_match not in line and count == 1:
                lines.append(line)
            elif pattern_to_match in line and count == 1:
                break

    # home = str(Path.home())
    # release_notes = os.path.join(home, "LATEST_RELEASE_NOTES.md")
    release_notes = os.path.join("../", "LATEST_RELEASE_NOTES.md")
    with open(release_notes, "w") as f:
        print("".join(lines), file=f, end="")
