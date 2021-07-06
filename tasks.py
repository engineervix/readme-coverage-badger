import os

from invoke import task


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


@task
def bump(c):
    """Use Commitizen Tools to bump version and generate changelog"""

    # TODO: this can be part of the "release" collection, where we bump, build and release
    c.run("cz bump --changelog", pty=True)


@task
def dist(c):
    """builds source and wheel package"""

    # TODO: provide a "clean" option, and improve portability
    c.run("python -m build", pty=True)
    c.run("ls -lah dist", pty=True)


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
