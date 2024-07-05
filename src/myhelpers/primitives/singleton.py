"""
This module provides a metaclass to turn a class into a singleton.
"""

from __future__ import annotations

from typing import ClassVar

__all__ = ['SingletonMeta']


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python.
    Some possible methods include: base class, decorator, metaclass.
    We will use the metaclass because it is best suited for this purpose.

    Copied from <https://refactoring.guru/design-patterns/singleton/python/example>

    For example,
    ```python
    class World(metaclass=SingletonMeta):
        pass

    world_a = World()
    world_b = World()
    assert world_a is world_b  # True
    ```
    """

    _instances: ClassVar[dict[type, object]] = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the [`__init__`][object.__init__] argument
        do not affect the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
