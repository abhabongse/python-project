import pytest

from mypackage.dummy import longest_common_prefix


@pytest.mark.parametrize(
    ("fst", "snd", "expected"),
    [
        ("", "", ""),
        ("", "abc", ""),
        ("abc", "", ""),
        ("xyz", "xyz", "xyz"),
        ("abcd", "ab", "ab"),
        ("wx", "wxyz", "wx"),
        ("abc", "xyz", ""),
        ("abcd", "abef", "ab"),
    ],
)
def test_longest_common_prefix(fst, snd, expected):
    assert longest_common_prefix(fst, snd) == expected
