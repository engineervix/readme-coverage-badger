# standard lib
import logging
import os
import sys
from urllib.parse import quote

import coverage

# third-party dependencies
import pytest
from colorama import Fore

from readme_coverage_badger import __main__

# local
from .conftest import TESTS_DIR


class MockCoverageError:
    """Mock coverage.misc.CoverageException"""

    def __init__(self, *args, **kwargs):
        raise coverage.misc.CoverageException


@pytest.fixture
def cb(monkeypatch):
    """
    Return a monkeypatched readme_coverage_badger module that
    always returns a percentage of 90.
    """

    def get_fake_total():
        return "90"

    monkeypatch.setattr(__main__, "get_total", get_fake_total)
    return __main__


@pytest.fixture
def no_total(monkeypatch):
    """
    Return a monkey patched readme_coverage_badger module that
    raises coverage.misc.CoverageException.
    """

    monkeypatch.setattr(__main__, "get_total", MockCoverageError)
    return __main__


def test_version(cb, capsys):
    """
    Test the version output.
    """
    with pytest.raises(SystemExit):
        cb.main(["-v"])
    out, _ = capsys.readouterr()
    assert out == "{}\n".format(__main__.__version__)


def test_successful_readme_coverage_badger(fake_readme, cb, caplog, monkeypatch):
    """
    Test that we can successfully generate a badge and update README.
    """
    readme_file = "README"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    cb.init()
    cb.configure_logging()
    cb.main([])
    caplog.set_level(logging.DEBUG)
    for record in caplog.records:
        assert record.levelname == "INFO"
    assert (
        f"{readme_file} has been successfully updated with the Coverage" in caplog.text
    )


def test_successful_readme_md_coverage_badger(fake_readme_md, cb, caplog, monkeypatch):
    """
    Test that we can successfully generate a badge and update README.md..
    """
    readme_file = "README.md"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    cb.init()
    cb.configure_logging()
    cb.main([])
    caplog.set_level(logging.DEBUG)
    for record in caplog.records:
        assert record.levelname == "INFO"
    assert (
        f"{readme_file} has been successfully updated with the Coverage" in caplog.text
    )


def test_no_readme_file(cb, caplog, monkeypatch):
    """
    Test behaviour when no README file exists in current directory
    """

    readme_file = "README.md"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    cb.init()
    cb.configure_logging()
    with pytest.raises(SystemExit) as e:
        cb.main([])
    caplog.set_level(logging.DEBUG)
    caplog_messages = [(record.levelname, record.msg) for record in caplog.records]
    valid_readmes = (
        f"{Fore.MAGENTA}README.md{Fore.RESET} or {Fore.MAGENTA}README{Fore.RESET}"
    )
    assert (
        "ERROR",
        f"There's no {valid_readmes} at this location",
    ) in caplog_messages
    assert (
        "INFO",
        f"Run this in a directory containing either a {valid_readmes} file",
    ) in caplog_messages
    assert e.type == SystemExit
    assert e.value.code == 1


def test_readme_no_replacement_string(
    fake_readme_no_replacement_str, cb, caplog, monkeypatch
):
    """
    Test behaviour when README file does not have any string of the form `![Code Coverage](.*?)`
    """
    readme_file = "README.md"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    cb.init()
    cb.configure_logging()
    with pytest.raises(SystemExit) as e:
        cb.main([])
    caplog.set_level(logging.DEBUG)
    caplog_messages = [(record.levelname, record.msg) for record in caplog.records]
    empty_badge_pattern = "![Code Coverage]()"
    help_message = Fore.MAGENTA + empty_badge_pattern + Fore.RESET
    assert (
        "WARNING",
        "I couldn't find anything to replace in your README file",
    ) in caplog_messages
    assert (
        "WARNING",
        f"please start by adding the following somewhere in your README: {help_message}",
    ) in caplog_messages
    assert e.type == SystemExit
    assert e.value.code == 0


def test_coverage_up_to_date(fake_readme_up_to_date, cb, caplog, monkeypatch):
    """
    Test behaviour when coverage badge in README file is already up-to-date
    """

    readme_file = "README.md"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    cb.init()
    cb.configure_logging()
    with pytest.raises(SystemExit) as e:
        cb.main([])
    caplog.set_level(logging.DEBUG)
    caplog_messages = [(record.levelname, record.msg) for record in caplog.records]
    assert (
        "INFO",
        f"Coverage in your {readme_file} is already up to date",
    ) in caplog_messages
    assert (
        "INFO",
        f"No changes made to your {readme_file}",
    ) in caplog_messages
    assert e.type == SystemExit
    assert e.value.code == 0


def test_no_coverage(fake_readme_md, no_total, caplog, monkeypatch):
    """
    Test behaviour when the script cannot not obtain any coverage
    """
    readme_file = "README.md"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    no_total.init()
    no_total.configure_logging()
    with pytest.raises(SystemExit) as excinfo:
        no_total.main([])
    caplog.set_level(logging.DEBUG)
    caplog_messages = [(record.levelname, record.msg) for record in caplog.records]
    assert (
        "ERROR",
        "Error: Did you run coverage first?",
    ) in caplog_messages
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 1


def test_coverage_is_none(fake_readme, cb, caplog, monkeypatch, mocker):
    """
    Test behaviour when, for some weird reason, coverage = None
    """

    mocker.patch.object(__main__, "coverage", None)
    readme_file = "README"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    cb.init()
    cb.configure_logging()
    with pytest.raises(SystemExit) as excinfo:
        cb.main([])

    caplog.set_level(logging.DEBUG)
    caplog_messages = [(record.levelname, record.msg) for record in caplog.records]
    availability = Fore.CYAN + str("coverage" in sys.modules) + Fore.RESET
    assert (
        "ERROR",
        f"Error: coverage returned 'None' ... checking availability on your system: {availability}",
    ) in caplog_messages
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 1


def test_colour_ranges(fake_readme, monkeypatch):
    """
    Whatever number we provide as coverage should produce the appropriate colour
    """

    readme_file = "README"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    for total, colour in (
        ("97", "brightgreen"),
        ("93", "green"),
        ("80", "yellowgreen"),
        ("65", "yellow"),
        ("45", "orange"),
        ("15", "red"),
        ("n/a", "lightgrey"),
    ):
        __main__.get_total = lambda: total
        __main__.main([])
        assert __main__.get_colour(total) == colour


def test_plain_colour_mode(fake_readme, caplog, monkeypatch):
    """
    Should always get one colour in badge
    """

    readme_file = "README"

    def fake_readme_location(*args, **kwargs):
        return os.path.join(TESTS_DIR, readme_file)

    monkeypatch.setattr(__main__, "readme_location", fake_readme_location)

    default_colour = __main__.DEFAULT_COLOUR
    assert default_colour == "green"
    for total in ("97.89", "93", "80", "65", "45", "15", "n/a"):
        __main__.get_total = lambda: total
        __main__.init()
        __main__.configure_logging()
        __main__.main(["-p"])
        caplog.set_level(logging.DEBUG)
        badge_url = f"https://img.shields.io/badge/Coverage-{total}{quote('%')}-{default_colour}.svg"
        with open(os.path.join(TESTS_DIR, readme_file), "r") as f:
            text = f.read()
            assert badge_url in text
