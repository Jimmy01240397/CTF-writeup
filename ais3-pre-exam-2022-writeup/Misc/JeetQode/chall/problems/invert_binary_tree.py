from __future__ import annotations
from problem import Problem
from typing import Any, Tuple, Union
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from random import randint


@dataclass_json
@dataclass
class Node:
    left: Union[Node, int]
    right: Union[Node, int]


Tree = Union[Node, int]


def gen_tree(depth) -> Tree:
    if randint(0, depth) == 0:
        return Node(gen_tree(depth + 1), gen_tree(depth + 1))
    return randint(1, 9)


def invert(t: Tree) -> Tree:
    if isinstance(t, int):
        return t
    else:
        return Node(invert(t.right), invert(t.left))


class InvertBinaryTree(Problem):
    @property
    def name(self) -> str:
        return "Invert Binary Tree"

    @property
    def desciption(self) -> str:
        return """
Input: A binary tree, where each leaf is an interger and node are objects with `left` and `right` property
Output: The inverted tree with `left` and `right` swapped, recursively

Examples:
Input: {"left": 1, "right": 3}
Output: {"left": 3, "right": 1}

Input: {"left": 1, "right": {"left": 1, "right": 3}}
Output: {"left": {"left": 3, "right": 1}, "right": 1}
"""

    @property
    def rounds(self) -> int:
        return 10

    def dumps(self, x):
        return x.to_json()

    def generate_testcase(self) -> Tuple[bool, Any]:
        t = Node(gen_tree(1), gen_tree(1))
        return t, invert(t)
