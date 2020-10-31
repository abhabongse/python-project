# Frequently Asked Questions

## What are differences between `requirements.in` and `requirements.txt`?

- `requirements.in` contains a list of python packages 
  we wish to install and use it directly.
- `requirements.txt` contains the pinned/locked down python packages
  which is the result of resolving package dependencies in `requirements.in`.

**Note:** For NodeJS programmers, an analogy for this would be `package.json`
vs `package-lock.json` files respectively.

This allows us to have _deterministic package installations_ across multiple machines,
which means that it is less likely one program works on one machine but not the other.

## Why are there multiple `requirements.txt` files in various python local packages?

In this project template, we demonstrate how programmers could separately maintain
python package dependencies for _different_ local python packages
(i.e. we have separate `myhelpers/requirements.txt` 
and `mypackage/requirements.txt` files).
This pattern is particularly useful if programmers need to build multiple docker images,
each with separate python package dependencies with space-efficient optimizations.

## What are differences between `requirements.txt` and `dev-requirements.txt`?

- `requirements.txt` contains a list of python packages
  explicitly used in the main codebase (via import statements).
- `dev-requirements.txt` contains a separate list of python packages
  assisting in software development process in local environment
  (but are _never_ used in the main codebase).

**Note:** For NodeJS programmers, an analogy for this would be `dependencies` 
vs `devDependencies` section in `package.json` file, respectively.

## Why does `Makefile` not assuming a particular `virtualenv` setup?

The tasks of creating and maintaining python `virtualenv` were left to individual 
preferences of python programmers (esp. critical in collaborative projects).
`Makefile` merely enforces that programmers must enter the virtualenv
before executing the scripts as a safeguard against preventable human misuse.
