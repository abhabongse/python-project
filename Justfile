# List all available commands
help:
    @just --list --unsorted

# ___                        _                    __  __           _
#|   \ ___ _ __  ___ _ _  __| |___ _ _  __ _  _  |  \/  |__ _ _ __| |_
#| |) / -_) '_ \/ -_) ' \/ _` / -_) ' \/ _| || | | |\/| / _` | '  \  _|
#|___/\___| .__/\___|_||_\__,_\___|_||_\__|\_, | |_|  |_\__, |_|_|_\__|
#         |_|                              |__/         |___/

# Export python dependencies in requirements.txt format at appropriate locations
export-python-packages:
    poetry export -f requirements.txt -o requirements.txt
    poetry export --with dev -f requirements.txt -o dev-requirements.txt
    poetry export --with docs -f requirements.txt -o docs/requirements.txt

#   ___         _        ___            _ _ _          _____         _
#  / __|___  __| |___   / _ \ _  _ __ _| (_) |_ _  _  |_   _|__  ___| |___
# | (__/ _ \/ _` / -_) | (_) | || / _` | | |  _| || |   | |/ _ \/ _ \ (_-<
#  \___\___/\__,_\___|  \__\_\\_,_\__,_|_|_|\__|\_, |   |_|\___/\___/_/__/
#                                               |__/

# Run tests against source files
check: ruff pyright pytest

# Format code using ruff
format:
    ruff check --fix && ruff format

# Check code with ruff
ruff +ARGS='check':
    ruff {{ARGS}}

# Type checking on all Python source files
pyright +ARGS='':
    pyright {{ARGS}}

# Run pytest against source files
pytest +ARGS='-v':
    poetry run python -m pytest {{ARGS}}

# Run pytest with line coverage checks
coverage +ARGS='-v':
    @echo Python packages: $(find src -maxdepth 2 -name '__init__.py' -printf '%h\n' | sed 's/^src\///')
    poetry run python -m pytest \
        $(find src -maxdepth 2 -name '__init__.py' -printf '%h\n' | sed 's/^src\//--cov=/') \
        --cov-report=term-missing {{ARGS}}

# Clear out all test files
[confirm]
cleantest:
    find . -name '.*_cache' -type d | xargs rm -rf
    rm -rf .coverage

#  ___
# |   \ ___  __ __ _ ___ _ _
# | |) / _ \/ _/ _` / -_) ' \
# |___/\___/\__\__, \___|_||_|
#              |___/

# Generate static-site documentation using mkdocs
docs:
    mkdocs build

# Live preview of documentation site
docs-dev:
    mkdocs serve

#  ___ _            _           _
# / __| |_  ___ _ _| |_ __ _  _| |_ ___
# \__ \ ' \/ _ \ '_|  _/ _| || |  _(_-<
# |___/_||_\___/_|  \__\__|\_,_|\__/__/
#

# Render markdown FILE
markdown FILE:
    poetry run python -m rich.markdown -w 119 {{FILE}}

# Syntax highlight source FILE
syntax FILE:
    poetry run python -m rich.syntax -l -r {{FILE}}

# Show git log tree
show-tree:
    @git --no-pager log --graph --abbrev-commit --decorate --all \
        --format=tformat:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'

#  ___        _     ___         _        _ _
# | _ \___ __| |_  |_ _|_ _  __| |_ __ _| | |
# |  _/ _ (_-<  _|  | || ' \(_-<  _/ _` | | |
# |_| \___/__/\__| |___|_||_/__/\__\__,_|_|_|
#

# Run this command after cloning the repo
post-install: install-pre-commit-hooks

# Install pre-commit hooks
install-pre-commit-hooks:
    pre-commit install
