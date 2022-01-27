# Python Project Template

Template for python project structure (with annotations).


## Features

- Uses [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)
  as project specification file per
  [PEP 518](https://www.python.org/dev/peps/pep-0518/),
  [PEP 517](https://www.python.org/dev/peps/pep-0517/),
  [PEP 621](https://www.python.org/dev/peps/pep-0621/), and
  [PEP 660](https://www.python.org/dev/peps/pep-0660/).
- Uses [Poetry](https://github.com/python-poetry/poetry)
  as build tools to manage package dependencies.
- Uses [Just](https://github.com/casey/just) for project-specific commands
  (e.g. for testing and linting tools, documentation generation).


## Local Development Setup

### 1. Poetry

Install Poetry to manage python virtual environments and package dependencies.
More information can be read from [Poetry documentation](https://python-poetry.org/docs/master/).

### 2. Base Python

If the required version of Python is not installed on the local development machine,
we recommend using `pyenv` to manage multiple installations of Python on the machine.

First, [following these instructions to install `pyenv`](https://github.com/pyenv/pyenv#installation).
For Linux distributions, we recommend the [automatic installer](https://github.com/pyenv/pyenv-installer) options.
Make sure to follow the instructions closely and add `pyenv` bin directories to `$PATH`.

Once installed, we can install the desired version of Python (we assume version `3.10.0` here):
```shell
$ pyenv install 3.10.0
```
- If `pyenv` command is not present, perhaps restart the terminal or machine first.
- If there are other problems while installing,
  [consult the troubleshooting page](https://github.com/pyenv/pyenv/wiki/common-build-problems).

### 3. Setup virtual environments

Use Poetry to create virtual environments and install dependencies:

```shell
$ poetry install --dev
```

### 4. Just

Install [Just](https://github.com/casey/just) to be able to run project-specific commands.
Once installed, you can see the list of commands by running:

```shell
$ just
```


## Git Commit Checklist

Before committing changes in Git Repository,
please run through the following checklist:

1. Run `just test` to test for code quality
   (such as `flake8` code lint, `pytest` unit tests, etc.)
   Fix any complaints until there is no error message.
2. Run `git status` to see the status of file changes.
   Verify with your eye that it is what is expected.
