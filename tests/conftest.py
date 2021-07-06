import logging
import os
import textwrap

import pytest
from faker import Faker

fake = Faker()

LOGGER = logging.getLogger(__name__)

TESTS_DIR = os.path.dirname(__file__)

MD_CONTENT = f"""\
# {fake.sentence().strip(".")}

{fake.text()}

[![MIT License](https://badgen.net/github/license/micromatch/micromatch)](https://github.com/micromatch/micromatch/blob/master/LICENSE)
[![Latest Release](https://badgen.net/gitlab/release/veloren/veloren)](https://github.com/veloren/veloren/releases)
![Code Coverage](whatever)

## Installation

{fake.text()}

```bash
pip install my-project
```

## Features

- {fake.sentence()}
- Light/dark mode toggle
- Live previews
- {fake.sentence()}
- Fullscreen mode
- Cross platform
- {fake.sentence()}

## Contributing

Contributions are always welcome!

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for ways to get started.

## Documentation

{fake.text()}

Check out the [detailed documentation]({fake.url()})

---

## Credits

This README was created with the help of <https://readme.so>.
"""


def generate_markdown_file(filename):
    """Generate a fake markdown file"""
    md_file = os.path.join(TESTS_DIR, filename)
    with open(md_file, mode="wt", encoding="utf-8") as readme_file:
        readme_file.write(textwrap.dedent(MD_CONTENT))


@pytest.fixture(scope="function")
def fake_readme():
    """Create a sample README file. Delete afterwards"""

    # Setup
    filename = "README"
    generate_markdown_file(filename)

    yield

    # Teardown / Cleanup
    try:
        os.remove(os.path.join(TESTS_DIR, filename))
    except OSError as ex:  # if failed, report it back to the user
        LOGGER.error(f"Error: {ex.filename} - {ex.strerror}.")


@pytest.fixture(scope="function")
def fake_readme_md():
    """Create a sample README.md file. Delete afterwards"""

    # Setup
    filename = "README.md"
    generate_markdown_file(filename)

    yield

    # Teardown / Cleanup
    try:
        os.remove(os.path.join(TESTS_DIR, filename))
    except OSError as ex:  # if failed, report it back to the user
        LOGGER.error(f"Error: {ex.filename} - {ex.strerror}.")


@pytest.fixture(scope="function")
def fake_readme_no_replacement_str():
    """Create a README.md file with no coverage badge. Delete afterwards"""

    # Setup
    filename = "README.md"
    md_file = os.path.join(TESTS_DIR, filename)
    with open(md_file, mode="wt", encoding="utf-8") as readme_file:
        readme_file.write(
            textwrap.dedent(MD_CONTENT.replace("![Code Coverage](whatever)", ""))
        )

    yield

    # Teardown / Cleanup
    try:
        os.remove(os.path.join(TESTS_DIR, filename))
    except OSError as ex:  # if failed, report it back to the user
        LOGGER.error(f"Error: {ex.filename} - {ex.strerror}.")


@pytest.fixture(scope="function")
def fake_readme_up_to_date():
    """Create a README.md file with already up-to-date coverage badge. Delete afterwards"""

    # Setup
    filename = "README.md"
    md_file = os.path.join(TESTS_DIR, filename)
    badge = "![Code Coverage](https://img.shields.io/badge/Coverage-90%25-green.svg)"
    with open(md_file, mode="wt", encoding="utf-8") as readme_file:
        readme_file.write(
            textwrap.dedent(MD_CONTENT.replace("![Code Coverage](whatever)", badge))
        )

    yield

    # Teardown / Cleanup
    try:
        os.remove(os.path.join(TESTS_DIR, filename))
    except OSError as ex:  # if failed, report it back to the user
        LOGGER.error(f"Error: {ex.filename} - {ex.strerror}.")
