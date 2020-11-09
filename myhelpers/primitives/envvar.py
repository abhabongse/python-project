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

ParseFunc = Callable[[Optional[str]], Any]
ValidateFunc = Callable[[Any], bool]

_FIELDS = '_envvar_fields_'


class EnvVariable:
    """
    Data descriptor for each environment variable
    defined within environment configuration class.

    An example below illustrates how to use this class::

        class ApplicationConfig:
            SECRET_KEY = EnvVariable(required=True, validate=lambda x: len(x) > 0)
            DELAY_SECONDS = EnvVariable(default=0, parse=int, validate=lambda x: x >= 0)
            FAUX_NAME = EnvVariable(env_name='REAL_NAME')

            def preload_all(self):
                '''
                Optionally call this method at the program start-up
                if you wish to pre-load all environment variables.
                Use this method is useful if you wish for your program to fail
                as earliest as possible when configuration is not complete.
                '''
                for key in self._envvar_fields_.keys():
                    getattr(self, key)

        conf = ApplicationConfig()
        conf.preload_all()

    Program containing the above code will accept environment variables
    **SECRET_KEY**, **DELAY_SECONDS**, and **REAL_NAME**, which can be accessed through
    ``conf.SECRET_KEY``, ``conf.DELAY_SECONDS``, and ``conf.FAUX_NAME``, respectively.

    Note that the owner class of these environment variable data descriptors
    will also automatically maintaining a dictionary mapping from attribute names
    to these data descriptors via ``_envvar_fields_`` class attribute.

    Attributes:
        attr_name: Name of the attribute tied to owner class
        env_name: Name of the environment variable.
            If this argument is not provided, this name will be borrowed from
            the name of the attribute tied to owner class.
            the variable name will be borrowed from the class attribute.
        required: Whether to expect the environment variable to be explicitly set
        default: This value will be used when the environment variable
            is unset and is not marked as required.
            It will be used as-is without parsing and validation.
        parse: If provided, must be a function which
            accepts the string value of the environment variable
            and converts it into any python value.
            For example, this function could be :func:`int` for integer conversion
            or :meth:`datetime.date.fromisoformat` for YYYY-MM-DD date object, etc.
        validate: If provided, must be a function which
            accepts the value and returns a boolean value
            whether the value is to be marked as validated.
            For example, to enforce that the parsed value must be positive,
            use ``lambda x: x > 0`` as the validation function.
    """
    attr_name: Optional[str]
    env_name: str
    required: bool
    default: Any
    parse: ParseFunc
    validate: ValidateFunc

    def __init__(
            self,
            env_name: str = None,
            required: bool = False,
            default: Any = None,
            parse: ParseFunc = None,
            validate: ValidateFunc = None,
    ):
        self.attr_name = None
        self.env_name = env_name
        self.required = required
        self.default = default
        self.parse = parse
        self.validate = validate

    def __get__(self, instance, owner_cls=None):
        if instance is None:
            return self
        if self.env_name not in instance.__dict__:
            instance.__dict__[self.env_name] = self._read_from_env()
        return instance.__dict__[self.env_name]

    def __set_name__(self, owner_cls, name):
        if self.attr_name:
            raise RuntimeError(
                f"cannot recycle the descriptor bound to attribute {name!r}, "
                f"previously bound to attribute {self.attr_name!r}",
            )
        self.attr_name = name
        self.env_name = self.env_name or name
        self._add_to_owner(owner_cls, name)

    def _read_from_env(self):
        value = os.getenv(self.env_name)
        if value is None:
            if self.required:
                raise RuntimeError(f"missing env variable: {self.env_name!r}")
            else:
                return self.default
        if self.parse:
            value = self.parse(value)
        if self.validate and not self.validate(value):
            if self.validate.__name__.isidentifier():
                func_alias = f" {self.validate.__qualname__}"
            else:
                func_alias = f"\n\t{inspect.getsource(self.validate).strip()}"
            raise RuntimeError(
                f"env variable {self.env_name!r} has the value {value!r} "
                f"which does not satisfy the validation function:{func_alias}",
            )
        return value

    def _add_to_owner(self, owner_cls, attr_name):
        if _FIELDS not in owner_cls.__dict__:
            fields = {}
            for parent in owner_cls.__mro__[-1:0:-1]:
                fields.update(getattr(parent, _FIELDS, {}))
            setattr(owner_cls, _FIELDS, fields)
        fields = getattr(owner_cls, _FIELDS)
        fields[attr_name] = self

    def __repr__(self):
        if self.env_name:
            cls_name = type(self).__qualname__
            return f"<{cls_name} env_name={self.env_name!r}>"
        return super().__repr__()
