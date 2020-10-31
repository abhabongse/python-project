# Python Project Template

Template for python project structure (with annotations).

## Features

- Works with vanilla virtualenv in order to manage the installation of 
  package package dependencies inside the local development machine.
- Development-only python package dependencies are maintained separately
  from those being used in the actual codebase
  (i.e. `dev-requirements.txt` as opposed to `requirements.txt`
  inside each root package such as `myhelpers` and `mypackage`).
- Maintains python requirements files separately for each root project package,
  hence allowing multiple docker images to be built separately
  with compacted installation of dependent python packages.
- `Makefile` for common python-related commands (such as for 
  python dependency management, testing and linting tools,
  documentation generation, etc.).

**For more information, see the guide of [how to use this template](docs/wiki/howto.md).**
