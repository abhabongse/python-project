"""
Dummy module to illustrate the python project structure.
"""
from __future__ import annotations


def longest_common_prefix(fst: str, snd: str) -> str:
    """
    Finds the longest prefix shared by both input strings.

    Args:
        fst: First string
        snd: Second string

    Returns:
        Longest common prefix string
    """
    bound = 0
    for a, b in zip(fst, snd):
        if a != b:
            break
        bound += 1
    return fst[:bound]
