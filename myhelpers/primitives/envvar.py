"""
This module provides a tool for defining
a list of environment variables accepted by the application
with a configuration-based pythonic syntax.
"""
from __future__ import annotations

import inspect
import os
from collections import Callable
from typing import Any, Optional

SanitizeFunc = Callable[[Optional[str]], Any]
ValidateFunc = Callable[[Any], bool]

_FIELDS = '_envvar_fields_'


class EnvironmentVariable:
    """
    Data descriptor for each environment variable defined within
    environment configuration extended from BaseEnvConfig.

    An example below illustrates how to use this class::

        class ApplicationConfig:
            SECRET_KEY = EnvironmentVariable(required=True, validate=lambda x: len(x) > 0)
            DELAY_SECONDS = EnvironmentVariable(default=0, sanitize=int, validate=lambda x: x >= 0)
            FAUX_NAME = EnvironmentVariable(env_name='REAL_NAME')

            def preload_all(self):
                '''
                Optionally call this method at the program start-up
                if you wish to pre-load all environment variables.
                '''
                for key in self._envvar_fields_.keys():
                    getattr(self, key)

        conf = ApplicationConfig()
        conf.preload_all()

    Program containing this code will accept environment variables
    **SECRET_KEY**, **DELAY_SECONDS**, and **REAL_NAME**, which can be accessed through
    ``conf.SECRET_KEY``, ``conf.DELAY_SECONDS``, and ``conf.FAUX_NAME``, respectively.

    Note that the owner class of these environment variable data descriptors
    will also automatically maintaining a dictionary mapping from attribute names
    to these data descriptors via ``_envvar_fields_`` class attribute.

    Attributes:
        env_name: Name of the environment variable
        required: Whether to expect the environment variable to be set
        default: This value will be used when the environment variable
            is unset and is not marked as required.
            It will be used as-is without sanitization and validation.
        sanitize: If provided, must be a function which
            accepts the string value of the environment variable
            and converts it into any python value.
            This function could be :func:`int` for integer conversion or
            :meth:`datetime.date.fromisoformat` for YYYY-MM-DD date object, etc.
        validate: If provided, must be a function which
            accepts the value and returns a boolean value
            whether the value is to be marked as validated.
            This function could be ``lambda x: x > 0`` for positive values, etc.
        attr_name: Name of the attribute tied to owner class.
    """
    env_name: str
    required: bool
    default: Any
    sanitize: SanitizeFunc
    validate: ValidateFunc
    attr_name: str

    def __init__(
            self,
            env_name: str = None,
            required: bool = False,
            default: Any = None,
            sanitize: SanitizeFunc = None,
            validate: ValidateFunc = None,
    ):
        self.env_name = env_name
        self.required = required
        self.default = default
        self.sanitize = sanitize
        self.validate = validate

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.env_name not in instance.__dict__:
            instance.__dict__[self.env_name] = self._read_from_env()
        return instance.__dict__[self.env_name]

    def __set_name__(self, owner, name):
        self.attr_name = name
        self.env_name = self.env_name or name
        self._add_to_owner(owner)

    def _read_from_env(self):
        value = os.getenv(self.env_name)
        if value is None:
            if self.required:
                raise RuntimeError(f"missing env variable: {self.env_name!r}")
            else:
                return self.default
        if self.sanitize:
            value = self.sanitize(value)
        if self.validate and not self.validate(value):
            if self.validate.__name__.isidentifier():
                func_alias = f" {self.validate.__qualname__}"
            else:
                func_alias = f"\n\t{inspect.getsource(self.validate).strip()}"
            raise RuntimeError(
                f"env variable {self.env_name!r} has the value {value!r} "
                f"which does not satisfy the validation function: {func_alias}"
            )
        return value

    def _add_to_owner(self, owner):
        if _FIELDS not in owner.__dict__:
            fields = {}
            for parent in owner.__mro__[-1:0:-1]:
                fields.update(getattr(parent, _FIELDS, {}))
            setattr(owner, _FIELDS, fields)
        fields = getattr(owner, _FIELDS)
        fields[self.attr_name] = self

    def __repr__(self):
        return f"<EnvironmentVariable env_name={self.env_name!r}>"
