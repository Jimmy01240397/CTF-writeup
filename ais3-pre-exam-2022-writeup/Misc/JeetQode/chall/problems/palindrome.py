from problem import Problem
from typing import Any, Tuple
from random import sample, randint
import string


def generate_random_string():
    if randint(0, 1):
        return "".join(sample(string.ascii_letters, 20))
    else:
        t = "".join(sample(string.ascii_letters, 10))
        return t + t[::-1]


class IsPalindrome(Problem):
    @property
    def name(self) -> str:
        return "Is Palindrome"

    @property
    def desciption(self) -> str:
        return """
Input: A string
Output: A boolean represents whether it is a palindrome

Examples:
Input: "aba"
Output: true

Input: "peko"
Output: false
"""

    @property
    def rounds(self) -> int:
        return 10

    def generate_testcase(self) -> Tuple[bool, Any]:
        s = generate_random_string()
        yes = s == s[::-1]
        return s, yes
