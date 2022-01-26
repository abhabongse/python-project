default:
    @just --list --unsorted

#   ___         _        ___            _ _ _          _____         _
#  / __|___  __| |___   / _ \ _  _ __ _| (_) |_ _  _  |_   _|__  ___| |___
# | (__/ _ \/ _` / -_) | (_) | || / _` | | |  _| || |   | |/ _ \/ _ \ (_-<
#  \___\___/\__,_\___|  \__\_\\_,_\__,_|_|_|\__|\_, |   |_|\___/\___/_/__/
#                                               |__/

test: flake8 pytest

flake8:
    poetry run flake8

pytest +ARGS='-v':
    poetry run python -m pytest {{ARGS}}

coverage +ARGS='-v':
    @echo Python packages: $(find src -maxdepth 2 -name '__init__.py' -printf '%h\n' | sed 's/^src\///')
    poetry run python -m pytest \
        $(find src -maxdepth 2 -name '__init__.py' -printf '%h\n' | sed 's/^src\//--cov=/') \
        --cov-report=term-missing {{ARGS}}

cleantest:
    find . -name '.*_cache' -type d | xargs rm -rf
    rm -rf .coverage

#  ___
# |   \ ___  __ __ _ ___ _ _
# | |) / _ \/ _/ _` / -_) ' \
# |___/\___/\__\__, \___|_||_|
#              |___/

docs BUILDER='help':
    poetry run sphinx-build -M {{BUILDER}} docs docs/_build

autodocs:
    poetry run sphinx-autobuild -b html docs docs/_build/livehtml

#  ___ _            _           _
# / __| |_  ___ _ _| |_ __ _  _| |_ ___
# \__ \ ' \/ _ \ '_|  _/ _| || |  _(_-<
# |___/_||_\___/_|  \__\__|\_,_|\__/__/
# 

markdown FILE:
    poetry run python -m rich.markdown -w 119 {{FILE}}

syntax FILE:
    poetry run python -m rich.syntax -l -r {{FILE}}

show-tree:
    @git --no-pager log --graph --abbrev-commit --decorate --all \
        --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'