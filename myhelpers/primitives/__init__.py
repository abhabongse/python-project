"""
Collection of primitive objects to help writing better python code.
"""
from __future__ import annotations

from myhelpers.primitives.envvar import EnvironmentVariable
from myhelpers.primitives.singleton import SingletonMeta

__all__ = [
    'EnvironmentVariable',
    'SingletonMeta',
]
