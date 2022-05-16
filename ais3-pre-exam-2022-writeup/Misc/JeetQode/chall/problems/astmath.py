from problem import Problem
from typing import Any, Tuple
from random import randint
import ast
import json


def gen_num():
    return str(randint(1, 9))


def gen_op():
    return "+-*/"[randint(0, 3)]


def gen_expr(depth):
    if randint(0, depth) == 0:
        l = gen_expr(depth + 1)
        r = gen_expr(depth + 1)
        op = gen_op()
        return f"({l}{op}{r})"
    return f"({gen_num()})"


class ASTMath(Problem):
    @property
    def name(self) -> str:
        return "AST Math"

    @property
    def desciption(self) -> str:
        return """
Input: An AST of Python's arithmetic expression (only +,-,*,/)
Output: Result number

Examples:
Input: {"body": {"left": {"value": 1, "kind": null, "lineno": 1, "col_offset": 0, "end_lineno": 1, "end_col_offset": 1}, "op": "<_ast.Add object at 0x7f0387ccde20>", "right": {"value": 2, "kind": null, "lineno": 1, "col_offset": 2, "end_lineno": 1, "end_col_offset": 3}, "lineno": 1, "col_offset": 0, "end_lineno": 1, "end_col_offset": 3}}
Output: 3

Input: {"body": {"left": {"left": {"value": 8, "kind": null, "lineno": 1, "col_offset": 1, "end_lineno": 1, "end_col_offset": 2}, "op": "<_ast.Mult object at 0x7f20eb76aee0>", "right": {"value": 7, "kind": null, "lineno": 1, "col_offset": 3, "end_lineno": 1, "end_col_offset": 4}, "lineno": 1, "col_offset": 1, "end_lineno": 1, "end_col_offset": 4}, "op": "<_ast.Sub object at 0x7f20eb76ae80>", "right": {"left": {"value": 6, "kind": null, "lineno": 1, "col_offset": 7, "end_lineno": 1, "end_col_offset": 8}, "op": "<_ast.Mult object at 0x7f20eb76aee0>", "right": {"value": 3, "kind": null, "lineno": 1, "col_offset": 9, "end_lineno": 1, "end_col_offset": 10}, "lineno": 1, "col_offset": 7, "end_lineno": 1, "end_col_offset": 10}, "lineno": 1, "col_offset": 0, "end_lineno": 1, "end_col_offset": 11}}
Output: 38
"""

    @property
    def rounds(self) -> int:
        return 10

    def dumps(self, x):
        return json.dumps(
            x, default=lambda x: x.__dict__ if len(x.__dict__) else str(x)
        )

    def generate_testcase(self) -> Tuple[bool, Any]:
        l = gen_expr(1)
        r = gen_expr(1)
        op = gen_op()
        expr = f"{l}{op}{r}"
        try:
            result = eval(expr)
        except ZeroDivisionError:
            return self.generate_testcase()
        return ast.parse(expr, mode="eval"), result
