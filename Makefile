#  __  __       _         __ _ _
# |  \/  | __ _| | _____ / _(_) | ___
# | |\/| |/ _` | |/ / _ \ |_| | |/ _ \
# | |  | | (_| |   <  __/  _| | |  __/
# |_|  |_|\__,_|_|\_\___|_| |_|_|\___|
#

# This function computes a list of dependent *requirements.txt files
# from *requirements.in file.
# Usage: $(call CONSTRAINED_REQFILES,<requirements.in>)
CONSTRAINED_REQFILES = \
	$(foreach req_file, \
		$(shell grep -oP '(?<=^-c\s).*' $(1) | sed 's/\s\+//g'), \
		$(join $(dir $(1)),$(req_file)) \
	)

# Locations to all requirement files that requires pinning down
REQUIREMENTS_FILES := requirements.txt
REQUIREMENTS_FILES += dev-requirements.txt

.PHONY: help
help:
	@# Show this help message
	@sed -n 'x;G;/^[^\S:]\+:.*\n\s*@#.*$$/{s/^\([^\S:]\+\):.*\n\s*@#\s*\(.\+\)$$/  \1 :: \2/;p;b};g;/^##@/{s/^##@\s*\(.*\)/'"\1"'/;p}' $(MAKEFILE_LIST) \
		| awk -F' :: ' 'BEGIN { printf "Usage: make \033[0;96m<target>\033[0m\n" } /^ / { printf "\033[0;96m%-30s\033[0m %s\n", $$1, $$2 } /^[^ ]/ { printf "\n\033[1m%s\033[0m\n", $$0 }'

################################
##@ Python Dependency Management
################################

.PHONY: install_python_packages
install_python_packages: $(REQUIREMENTS_FILES)
	@# Install python packages in current virtual environment
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	@which pip-sync >/dev/null 2>&1 || pip install pip-tools
	pip-sync $(REQUIREMENTS_FILES)

.PHONY: lock_python_requirements
lock_python_requirements: $(REQUIREMENTS_FILES)
	@# Pin down python package dependencies as *-requirements.txt files

# NOTE: another second expansion prerequisites at the bottom of this Makefile
$(REQUIREMENTS_FILES): %.txt: %.in
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	@which pip-compile >/dev/null 2>&1 || pip install pip-tools
	pip-compile -o $@ $<
	@echo "Generated $@ from $^"

######################
##@ Code Quality Tools
######################

.PHONY: test
test: flake8 pytest mypy
	@# Run all code quality tools

.PHONY: flake8
flake8:
	@# Run flake8 python code linter tool
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	flake8

.PHONY: pytest
pytest:
	@# Run python unit tests (you may also specify ARGS='<pytest args>')
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	python -m pytest $(ARGS)

.PHONY: mypy
mypy:
	@# Run python type checker tool
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	mypy .

#####################
##@ Program Shortcuts
#####################

.PHONY: git_show_tree
git_show_tree:
	@# Show git commit history as a nice tree
	@git log --graph --abbrev-commit --decorate --all \
		--format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'

.PHONY: jnb
jnb:
	@# Launch jupyter notebook inside environment
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	jupyter notebook

.PHONY: jc
jc:
	@# Launch jupyter console inside environment
ifndef VIRTUAL_ENV
	$(error must run target inside python virtualenv)
endif
	jupyter console

###################
## Second Expansion
###################

.SECONDEXPANSION:
$(REQUIREMENTS_FILES): %.txt: $$(call CONSTRAINED_REQFILES,$$<)
