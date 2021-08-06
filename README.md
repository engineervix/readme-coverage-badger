<h1 align="center">Welcome to README Coverage Badger 👋</h1>

<p align="center">
<a href="https://pypi.python.org/pypi/readme-coverage-badger" target="_blank">
  <img src="https://img.shields.io/pypi/v/readme-coverage-badger.svg" alt="PyPi">
</a>
<a href="https://pypi.org/project/readme-coverage-badger" target="_blank">
  <img src="https://img.shields.io/pypi/pyversions/readme-coverage-badger" alt="PyPI - Python Version">
</a>
<a href="https://github.com/engineervix/readme-coverage-badger/actions/workflows/main.yml" target="_blank">
  <img src="https://github.com/engineervix/readme-coverage-badger/actions/workflows/main.yml/badge.svg" alt="Build Status">
</a>
<a href="https://codecov.io/gh/engineervix/readme-coverage-badger" target="_blank">
  <img src="https://codecov.io/gh/engineervix/readme-coverage-badger/branch/master/graph/badge.svg" alt="codecov">
</a>
<a href="https://results.pre-commit.ci/latest/github/engineervix/readme-coverage-badger/master" target="_blank">
  <img src="https://results.pre-commit.ci/badge/github/engineervix/readme-coverage-badger/master.svg" alt="pre-commit.ci status">
</a>
<a href="https://pyup.io/repos/github/engineervix/readme-coverage-badger/" target="_blank">
  <img src="https://pyup.io/repos/github/engineervix/readme-coverage-badger/shield.svg" alt="Updates">
</a>
<a href="https://pypi.org/project/readme-coverage-badger" target="_blank">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/readme-coverage-badger">
</a>
<a href="https://github.com/engineervix/readme-coverage-badger/commits/master" target="_blank">
  <img alt="GitHub commits since latest release (by SemVer)" src="https://img.shields.io/github/commits-since/engineervix/readme-coverage-badger/latest/master">
</a>
</p>

<p align="center">
<a href="https://opensource.org/licenses/BSD-3-Clause">
  <img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" alt="License">
</a>
<a href="https://github.com/psf/black">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
</a>
<a href="https://conventionalcommits.org">
  <img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square" alt="Conventional Commits">
</a>
<a href="https://commitizen-tools.github.io/commitizen/">
  <img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg" alt="Commitizen friendly">
</a>
</p>

> Generates a coverage badge using coverage.py and the shields.io service. Your README file is then updated with the generated badge.

<p align="center">
  <img src="https://github.com/engineervix/readme-coverage-badger/blob/assets/demo.gif" alt="demo.gif">
</p>
<!-- ![demo.gif](../assets/demo.gif?raw=true) -->

**Source Code**: [github.com/engineervix/readme-coverage-badger](https://github.com/engineervix/readme-coverage-badger)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Why this project?](#why-this-project)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [💻 Development](#-development)
  - [First things first](#first-things-first)
  - [Getting Started](#getting-started)
  - [Tests](#tests)
  - [Code Formatting](#code-formatting)
- [Author](#author)
- [🤝 Contributing](#-contributing)
- [Show your support](#show-your-support)
- [✅ TODO](#-todo)
  - [core](#core)
  - [docs](#docs)
  - [other](#other)
- [📝 License](#-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Why this project?

There are so many excellent coverage badge generation tools out there, why do we need another one? Well, at the time of writing this package (circa early 2021), all the existing tools (for example, [coverage-badge](https://github.com/dbrgn/coverage-badge)) I had come across ended at generating SVG/PNG files/strings/Base64 images. What you do with this remains entirely up to you.

Now, it is often much easier to simply use online services such as [codecov.io](https://about.codecov.io/) and [coveralls.io](https://coveralls.io/). These services are free for open source projects, but require a monthly subscription for private repos. Many times, we work on private repos, and we wanna be able to automatically have coverage badges in our READMEs. What if you are unable to pay such subscription fees, or maybe you don't want to use a SaaS? Your solution becomes to generate your own badge!

This is where this project comes in. It **automatically generates your project's coverage badge using the [shields.io](https://shields.io/) service, and then updates your README** accordingly, in just one command! That's all it does, resonating with the Unix philosophy of doing one thing and doing it well. The main idea for this came from [istanbul-badges-readme](https://github.com/olavoparno/istanbul-badges-readme), which does exactly the same thing for JavaScript projects. You will see that these two projects have quite a lot in common.

After using [istanbul-badges-readme](https://github.com/olavoparno/istanbul-badges-readme), I searched for a python alternative but couldn't find anything suitable. The closest I found was [coverage-badge](https://github.com/dbrgn/coverage-badge), and if you look at this project's code, you will see a lot of similarities with [coverage-badge](https://github.com/dbrgn/coverage-badge)!

If what you're looking for is a powerful, _general purpose badge generation tool_ for your projects, then you should probably check out projects like [anybadge](https://github.com/jongracecox/anybadge) and [genbadge](https://github.com/smarie/python-genbadge/).

## Features

- automatically generates your project's coverage badge using the [shields.io](https://shields.io/) service, and then updates your project's README with the newly generated badge
- simple CLI tool (`readme-cov`) with helpful messages
- tested on python 3.6 to 3.9 with coverage ≥ 84%
- free software: BSD-3-Clause license
- generates different colours depending on the coverage percentage. Optionally generate plain colour (green) regardless of percentage
- minimal external dependencies – this tool only has 2 external dependencies; [Coverage.py](https://github.com/nedbat/coveragepy) (obviously!) and [colorama](https://github.com/tartley/colorama) (for cross-platform coloured terminal output)

The table below shows the coverage thresholds, associated colours and examples of generated badges:

| Coverage            | Colour      | Example                                                                                    |
|---------------------|-------------|--------------------------------------------------------------------------------------------|
| 0 ≤ coverage < 40   | red         | ![Code Coverage Red ](https://img.shields.io/badge/Coverage-13%25-red.svg)                 |
| 40 ≤ coverage < 60  | orange      | ![Code Coverage Orange ](https://img.shields.io/badge/Coverage-46%25-orange.svg)           |
| 60 ≤ coverage < 75  | yellow      | ![Code Coverage Yellow ](https://img.shields.io/badge/Coverage-69%25-yellow.svg)           |
| 75 ≤ coverage < 90  | yellowgreen | ![Code Coverage Yellow Green](https://img.shields.io/badge/Coverage-85%25-yellowgreen.svg) |
| 90 ≤ coverage < 95  | green       | ![Code Coverage Green](https://img.shields.io/badge/Coverage-91%25-green.svg)              |
| 95 ≤ coverage ≤ 100 | brightgreen | ![Code Coverage Bright Green](https://img.shields.io/badge/Coverage-96%25-brightgreen.svg) |

## Installation

```sh
pip install readme-coverage-badger
```

## Usage

**Note**: Before using the tool, ensure that you insert a string of the form `![Code Coverage]()` or `![Code Coverage](anything here)` in your project's README.

```txt
readme-cov [-h] [-v] [-p]

optional arguments:
  -h, --help     show the help message and exit
  -v, --version  show program's version number and exit
  -p, --plain    Plain colour mode. Standard green badge.
```

The tool operates on the basis of the following assumptions:

- you have a README.md or README file at the root of your project
- your README file is in markdown format. I know, some Pythonistas prefer restructuredtext! Sadly, this isn't supported (yet)
- Somewhere in your your README is a string in the form: `![Code Coverage]()` or `![Code Coverage](anything here)`. This is what gets updated in-place (using [`re.sub()`](https://docs.python.org/3.8/library/re.html#re.sub)) when the script runs.
- the script is called from the root of your project repo, which has coverage.py already configured, and the coverage already updated (you have already run your tests prior to running the script)
- If the coverage badge in your README file is already up to date, your README file won't be updated, you will only be notified

## 💻 Development

### First things first

- ensure that you have [Python 3.6+](https://www.python.org/) on your machine, and that you are able to configure python [**virtual environment**](https://realpython.com/python-virtual-environments-a-primer/)s.
- ensure that you have [git](https://git-scm.com/) setup on your machine.

### Getting Started

First, [fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) this repository, then fire up your command prompt and ...

1. Clone the forked repository
2. Navigate to the cloned project directory: `cd readme_coverage_badger`
3. activate your python virtual environment and `pip install --upgrade pip`
4. Install dependencies: `pip install -r requirements_dev.txt`
5. Setup [pre-commit](https://pre-commit.com/) by running `pre-commit install` followed by `pre-commit install --hook-type commit-msg`. Optionally run `pre-commit run --all-files` to make sure your pre-commit setup is okay.

At this stage, hopefully everything should be working fine, and you should be able to start hacking on the project.

You can run the application via `invoke run` or

```sh
python readme_coverage_badger/__main__.py
```

### Tests

Simply run `pytest` or `invoke test` to run tests in your virtual environment.

Test other Python versions by running `tox`.

### Code Formatting

- Run `invoke lint` to run [`flake8`](https://flake8.pycqa.org/en/latest/), [`black`](https://black.readthedocs.io/en/stable/), [`isort`](https://pycqa.github.io/isort/) and [`mypy`](https://mypy.readthedocs.io/en/stable/) on the code.
- If you get any errors from `black` and/or `isort`, run `invoke lint --fix` or `invoke lint -f` so that black and isort can format your files. Alternatively, just run `pre-commit`. You can take a look at [.pre-commit-config.yaml](https://github.com/engineervix/readme-coverage-badger/blob/master/.pre-commit-config.yaml).

## Author

👤 **Victor Miti**

- Blog: <https://importthis.tech>
- Twitter: [![Twitter: engineervix](https://img.shields.io/twitter/follow/engineervix.svg?style=social)](https://twitter.com/engineervix)
- Github: [@engineervix](https://github.com/engineervix)

## 🤝 Contributing

Contributions, issues and feature requests are most welcome! A good place to start is by helping out with the unchecked items in the [TODO](#-todo) section of this README!

Feel free to check the [issues page](https://github.com/engineervix/readme-coverage-badger/issues) and take a look at the [contributing guide](https://github.com/engineervix/readme-coverage-badger/blob/master/CONTRIBUTING.md) before you get started. In addition, please note the following:

- if you're making code contributions, please try and write some tests to accompany your code, and ensure that the tests pass. Also, were necessary, update the docs so that they reflect your changes.
- commit your changes via `cz commit`. Follow the prompts. When you're done, `pre-commit` will be invoked to ensure that your contributions and commits follow defined conventions. See `pre-commit-config.yaml` for more details.
- your commit messages should follow the conventions described [here](https://www.conventionalcommits.org/en/v1.0.0/). Write your commit message in the imperative: "Fix bug" and not "Fixed bug" or "Fixes bug." This convention matches up with commit messages generated by commands like `git merge` and `git revert`.
Once you are done, please create a [pull request](https://github.com/engineervix/readme-coverage-badger/pulls).

## Show your support

Please give a ⭐️ if this project helped you!

## ✅ TODO

### core

- [ ] Cater for not only markdown but also restructuredtext, and automatically detect if a file's syntax is markdown or restructuredtext if no extension given
- [ ] Provide option to generate badge in HTML format
- [ ] Provide option to generate to `stdout` and skip substitution in a README file. This could be useful if you're using the tool in a script and you just want the result so that you can use it elsewhere.
- [ ] Allow for flexibility in choosing whatever colours one wants
- [ ] Allow for specifying *Alt Text* on the badge URL, for example `![Alt Text]()` or `![Alt Text](anything here)`
- [ ] Make the codebase fully typed
- [ ] Improve the Tests by [parametrizing](https://docs.pytest.org/en/stable/example/parametrize.html) fixtures and test functions
- [X] improve CI/CD to cater for GNU/Linux, Mac OS X and Windows
- [ ] Create pre-commit hook

### docs

- [X] Add a screenshot / demo in this README
- [ ] Create standalone documentation for hosting either on Github Pages or readthedocs. This README is already detailed enough to serve as documentation!

### other

- [ ] It would be fun if we had some kind of a [badger](https://en.wikipedia.org/wiki/Badger) logo!

## 📝 License

Copyright © 2021 [Victor Miti](https://github.com/engineervix).

This project is licensed under the terms of the [BSD-3-Clause](https://github.com/engineervix/readme-coverage-badger/blob/main/LICENSE) license.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
***
