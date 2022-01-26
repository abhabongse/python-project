default:
    @just --list --unsorted

#   ___         _        ___            _ _ _          _____         _
#  / __|___  __| |___   / _ \ _  _ __ _| (_) |_ _  _  |_   _|__  ___| |___
# | (__/ _ \/ _` / -_) | (_) | || / _` | | |  _| || |   | |/ _ \/ _ \ (_-<
#  \___\___/\__,_\___|  \__\_\\_,_\__,_|_|_|\__|\_, |   |_|\___/\___/_/__/
#                                               |__/

test: flake8 pytest

flake8:
    #!/usr/bin/env bash
    set -e
    if [ -z ${VIRTUAL_ENV+x} ]; then
        echo >&2 "error: required python venv"
        exit 1
    fi
    flake8

pytest +ARGS='-v':
    #!/usr/bin/env bash
    set -e
    if [ -z ${VIRTUAL_ENV+x} ]; then
        echo >&2 "error: required python venv"
        exit 1
    fi
    python -m pytest {{ARGS}}

coverage +ARGS='-v':
    #!/usr/bin/env bash
    set -e
    if [ -z ${VIRTUAL_ENV+x} ]; then
        echo >&2 "error: required python venv"
        exit 1
    fi
    PYTHON_PROJECT_PACKAGES="$(find . -maxdepth 2 -name '__init__.py' -printf '%h\n' | cut -d/ -f2- | sed 's/^/--cov=/')"
    python -m pytest $PYTHON_PROJECT_PACKAGES --cov-report=term-missing {{ARGS}}

cleantest:
    find . -name '.*_cache' -type d | xargs rm -rf
    rm -rf .coverage

#  ___
# |   \ ___  __ __ _ ___ _ _
# | |) / _ \/ _/ _` / -_) ' \
# |___/\___/\__\__, \___|_||_|
#              |___/

docs BUILDER='help':
    #!/usr/bin/env bash
    set -e
    if [ -z ${VIRTUAL_ENV+x} ]; then
        echo >&2 "error: required python venv"
        exit 1
    fi
    sphinx-build -M {{BUILDER}} docs docs/_build

autodocs:
    #!/usr/bin/env bash
    set -e
    if [ -z ${VIRTUAL_ENV+x} ]; then
        echo >&2 "error: required python venv"
        exit 1
    fi
    sphinx-autobuild -b html docs docs/_build/livehtml

#  ___ _            _           _
# / __| |_  ___ _ _| |_ __ _  _| |_ ___
# \__ \ ' \/ _ \ '_|  _/ _| || |  _(_-<
# |___/_||_\___/_|  \__\__|\_,_|\__/__/
# 

markdown FILE:
    @python -m rich.markdown -w 119 {{FILE}}

syntax FILE:
    @python -m rich.syntax -l -r {{FILE}}

show-tree:
    @git --no-pager log --graph --abbrev-commit --decorate --all \
        --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'
