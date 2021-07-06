#!/usr/bin/env python3

"""README Coverage Badger

Generates a coverage badge using coverage.py and the shields.io service.
Your README/README.md file is then updated with the generated badge.

Requires that `coverage` and `colorama` be installed within the Python
environment you are running this script in.
"""

__version__ = "0.1.0"


# Python Standard Library
import argparse
import copy
import logging
import os
import re
import sys
from pathlib import Path
from traceback import format_exception
from typing import Optional, Union
from urllib.parse import quote

# coverage.py
import coverage

# other external dependency
from colorama import Fore, Style, init

# specify colors for different logging levels
LOG_COLORS = {
    # logging.DEBUG: Fore.WHITE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    # logging.CRITICAL: Fore.RED,
}


class ColourFormatter(logging.Formatter):
    """Display the severity of the log using unique colours

    Credits:
        https://uran198.github.io/en/python/2016/07/12/colorful-python-logging.html
    """

    def format(self, record, *args, **kwargs):
        """
        if the corresponding logger has children, they may receive modified
        record, so we want to keep it intact
        """
        new_record = copy.copy(record)
        if new_record.levelno in LOG_COLORS:
            # we want levelname to be in different color, so let's modify it
            new_record.levelname = "{color_begin}{level}{color_end}".format(
                level=new_record.levelname,
                color_begin=LOG_COLORS[new_record.levelno],
                color_end=Style.RESET_ALL,
            )
        # now we can let standart formatting take care of the rest
        return super(ColourFormatter, self).format(new_record, *args, **kwargs)


class Devnull(object):
    """A file like object that does nothing.

    Credits:
        https://github.com/dbrgn/coverage-badge
    """

    def write(self, *args, **kwargs):
        pass


def configure_logging():
    """Logging configuration for the project"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # we want to display levelname, asctime and message
    formatter = ColourFormatter(
        "%(levelname)-12s: %(asctime)-8s %(message)s", datefmt="%d-%b-%y %H:%M:%S"
    )

    # this handler will write to sys.stdout by default
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    # adding handler to our logger
    logger.addHandler(handler)


def log_traceback(ex):
    """Logs Errors
    Args:
        ex:
            An Exception instance.
    """
    tb_lines = format_exception(ex.__class__, ex, ex.__traceback__)
    tb_text = "".join(tb_lines)
    logging.error(tb_text)


def get_total():
    """
    Return the rounded total as properly rounded string.

    Credits:
        https://github.com/dbrgn/coverage-badge
    """
    cov = coverage.Coverage()
    cov.load()
    total = cov.report(file=Devnull())

    class Precision(coverage.results.Numbers):
        """
        A class for using the percentage rounding of the main coverage package,
        with any percentage.
        To get the string format of the percentage, use the ``pc_covered_str``
        property.
        """

        def __init__(self, percent):
            self.percent = percent

        @property
        def pc_covered(self):
            return self.percent

    return Precision(total).pc_covered_str


DEFAULT_COLOUR = "green"

COLOUR_RANGES = [
    (95, "brightgreen"),
    (90, "green"),
    (75, "yellowgreen"),
    (60, "yellow"),
    (40, "orange"),
    (0, "red"),
]


def get_colour(total):
    """Return colour for current coverage percent
    Args:
        total:
            total coverage (str).
    """
    try:
        xtotal = int(total)
    except ValueError:
        return "lightgrey"
    for range_, colour in COLOUR_RANGES:
        if xtotal >= range_:
            return colour


def get_badge(total, colour=DEFAULT_COLOUR):
    """update total and return shields.io URL
    Args:
        total:
            total coverage (str).
        colour:
            badge colour (str).
    """
    percent = quote("%")
    shields_badge = (
        f"https://img.shields.io/badge/Coverage-{total}{percent}-{colour}.svg"
    )
    return shields_badge


def readme_location(filename: Union[str, str] = "README.md") -> Path:
    """Path to the README file"""
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parents[0]
    readme_file = parent_dir / filename

    return readme_file


def update_coverage_badge(readme: Path, cov_string: str, plain: Optional[bool] = False):
    """update coverage badge in a readme file

    Args:
        readme (Path): readme file where we'll perform in-place substitution
        cov_string (str): total test coverage
        plain (bool): whether to use plain colour or not
    """
    readme_file = readme
    total = cov_string
    colour = DEFAULT_COLOUR if plain else get_colour(total)
    badge = get_badge(total, colour)

    empty_badge_pattern = "![Code Coverage]()"
    existing_badge_pattern = r"\!\[Code Coverage\]\(.*?\)"
    patterns_to_match = rf"{re.escape(empty_badge_pattern)}|{existing_badge_pattern}"
    replacement_str = f"![Code Coverage]({badge})"

    try:
        with open(readme_file, "r+") as f:
            text = f.read()
            if replacement_str in text:
                logging.info(
                    f"Coverage in your {Path(readme).name} is already up to date"
                )
                logging.info(f"No changes made to your {Path(readme).name}")
                sys.exit(0)
            elif bool(re.search(patterns_to_match, text)) is False:
                logging.warning(
                    "I couldn't find anything to replace in your README file"
                )
                help_message = Fore.MAGENTA + empty_badge_pattern + Fore.RESET
                logging.warning(
                    f"please start by adding the following somewhere in your README: {help_message}"
                )
                sys.exit(0)
            else:
                updated_text = re.sub(patterns_to_match, replacement_str, text)
                f.seek(0)
                f.write(updated_text)
                f.truncate()
                logging.info(
                    f"{Path(readme).name} has been successfully updated with the Coverage"
                )
    except IOError as ex:
        logging.error("Error encountered while reading file ...")
        log_traceback(ex)


def main(args=None):
    """Console script entry point"""

    init()
    configure_logging()

    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="readme-cov",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.version = __version__
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "-p",
        "--plain",
        dest="plain_colour",
        action="store_true",
        help="Plain colour mode. Standard green badge.",
    )

    args = parser.parse_args(args)

    # Check for coverage
    if coverage is None:
        availability = Fore.CYAN + str("coverage" in sys.modules) + Fore.RESET
        logging.error(
            f"Error: coverage returned 'None' ... checking availability on your system: {availability}"
        )
        sys.exit(1)

    # check total coverage
    try:
        total = get_total()
    except coverage.misc.CoverageException as ex:
        logging.error("Error: Did you run coverage first?")
        log_traceback(ex)
        sys.exit(1)

    # Generate badge
    readme_md_file = readme_location("README.md")
    readme_file = readme_location("README")
    if os.path.exists(readme_md_file):
        update_coverage_badge(readme_md_file, total, args.plain_colour)
    elif os.path.exists(readme_file):
        update_coverage_badge(readme_file, total, args.plain_colour)
    else:
        valid_readmes = (
            f"{Fore.MAGENTA}README.md{Fore.RESET} or {Fore.MAGENTA}README{Fore.RESET}"
        )
        logging.error(f"There's no {valid_readmes} at this location")
        logging.info(
            f"Run this in a directory containing either a {valid_readmes} file",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
