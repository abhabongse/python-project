# How To Use This Template

## Local Development Setup

1. Install a specific version of python 3 (recommended using `pyenv`)
   and use it create a new virtualenv.  
   [For more information, click here.](pyenv.md)
2. Inside the virtualenv,
   run the following to install all required python packages
   ```bash
   (venv)$ make install_python_packages
   ```

## Customization

[Read how to customize this python project template.](customize.md)


## Git Commit Checklist

Before committing changes in Git Repository, 
please run through the following checklist:

1. Run `make test` to test for code quality
   (such as `flake8` code lint, `pytest` unit tests, etc.)
   Fix any complaints until there is no error message.
2. Run `git status` to see the status of file changes.
   Verify with your eye that it is what is expected.


## Useful Makefile Commands

### List all make commands

```bash
(venv)$ make  # or make help
```

### Install new python packages

To install a new python package (or update the version of existing ones),
modify the file `requirements.in` (or `dev-requirements.in`; see FAQ)
and run the following to pin down packages and install.
```bash
(venv)$ make lock_python_requirements && make install_python_packages
```

## Frequently Asked Questions

[See here](faqs.md).
