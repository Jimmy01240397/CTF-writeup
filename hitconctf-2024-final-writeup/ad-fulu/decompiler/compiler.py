#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import sys
import hashlib
import glob
from copy import copy, deepcopy
import base64
import json
import os
import hmac
import hashlib
from db import connect
import random
import re
import time
import aggdraw
from urllib.parse import urlparse, parse_qs
import ast
import interpreter
import random

class Compiler(ast.NodeVisitor):
    def __init__(self, fulus, funcname = None):
        self.funcname = funcname
        self.opcodes = {'': ''}
        self.fulus = fulus
        self.varmap = {}
        if funcname != None:
            for a in self.fulus[funcname].variables:
                self.varmap[f'_{a[:8]}'] = a

    def compile(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        return self.opcodes

    def visit_FunctionDef(self, node):
        compiler = Compiler(self.fulus, node.name)
        for stmt in node.body:
            compiler.visit(stmt)
        self.opcodes[node.name] = compiler.opcodes['']
        #for a in node.body:
        #    print(dir(a.targets[0]))
        #    print(a.targets[0].id)

    def visit_Pass(self, node):
        pass

    def visit_Assign(self, node):
        self.opcodes[''] += '狋'
        self.visit(node.targets[0])
        self.opcodes[''] += "竺"
        self.visit(node.value)
        self.opcodes[''] += "川"

    def visit_Name(self, node):
        if node.id == 'arg1':
            self.opcodes[''] += '肖'
            return
        if node.id == 'arg2':
            self.opcodes[''] += '余'
            return
        if node.id == 'arg3':
            self.opcodes[''] += '槐'
            return
        
        self.opcodes[''] += '䊆'
        if node.id not in self.varmap:
            self.varmap[node.id] = random.randbytes(64).hex()
        self.opcodes[''] += self.varmap[node.id]

    def visit_Constant(self, node):
        self.opcodes[''] += "䔃"
        if type(node.value) == int:
            self.opcodes[''] += "䔃腓"
            self.opcodes[''] += str(node.value)
        elif type(node.value) == float:
            self.opcodes[''] += "䔃拋"
            self.opcodes[''] += str(node.value)
        elif type(node.value) == str:
            self.opcodes[''] += "䔃𤞞"
            self.opcodes[''] += str(node.value)
        elif type(node.value) == bool:
            self.opcodes[''] += "䔃蛶"
            self.opcodes[''] += str(node.value)
        elif type(node.value) == bytes:
            self.opcodes[''] += "䔃尥"
            self.opcodes[''] += node.value.hex()
        elif type(node.value) == type(None):
            self.opcodes[''] += "䔃𢏗陲"
        else:
            raise
        self.opcodes[''] += "陲"

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            self.opcodes[''] += "若"
            idx = 0
            for arg in node.args:
                self.visit(arg)
                self.opcodes[''] += "瀳" if idx % 2 == 0 else "適"
            if self.opcodes[''][-1] == '瀳':
                self.opcodes[''] = self.opcodes[''][:-1]
            self.opcodes[''] += "喱"
            return

        self.opcodes[''] += '拑'
        for arg in node.args:
            self.visit(arg)
            self.opcodes[''] += "塺"
        if self.opcodes[''][-1] == "塺":
            self.opcodes[''] = self.opcodes[''][:-1]
        self.opcodes[''] += "韔"
        current = node.func
        if isinstance(current, ast.Attribute):
            while isinstance(current, ast.Attribute):
                self.opcodes[''] += current.attr
                self.opcodes[''] += "巜"
                current = current.value
            self.visit(current)
        else:
            if current.id == 'print':
                pass
            else:
                self.opcodes[''] += current.id
        self.opcodes[''] += "趹"

    def visit_If(self, node):
        self.opcodes[''] += "飧"
        self.visit(node.test)
        self.opcodes[''] += "嗔"
        for stmt in node.body:
            self.visit(stmt)
        self.opcodes[''] += "𪊨"
        if node.orelse:
            for stmt in node.orelse:
                self.visit(stmt)
        self.opcodes[''] += "婬"

    def visit_Compare(self, node):
        if isinstance(node.ops[0], ast.Eq):
            self.opcodes[''] += "𧢼"
        elif isinstance(node.ops[0], ast.NotIn):
            self.opcodes[''] += "㸹"
        elif isinstance(node.ops[0], ast.Gt):
            self.opcodes[''] += "㠭"
        elif isinstance(node.ops[0], ast.GtE):
            self.opcodes[''] += "漦"
        elif isinstance(node.ops[0], ast.LtE):
            self.opcodes[''] += "𥄉"
        elif isinstance(node.ops[0], ast.NotEq):
            self.opcodes[''] += "𥄕"
        else:
            raise

        left = self.visit(node.left)
        self.opcodes[''] += '盭'
        right = self.visit(node.comparators[0])

    def visit_Return(self, node):
        self.opcodes[''] += '䫶'
        if node.value:
            self.visit(node.value)

    def visit_Subscript(self, node):
        if isinstance(node.slice, ast.Slice):
            self.opcodes[''] += '嵞'
            self.visit(node.value)
            self.opcodes[''] += '慇'
            if node.slice.lower:
                self.visit(node.slice.lower)
            self.opcodes[''] += '𦝠'
            if node.slice.upper:
                self.visit(node.slice.upper)
            self.opcodes[''] += '騢'
        else:
            self.opcodes[''] += '誋'
            self.visit(node.value)
            self.opcodes[''] += '𦵹'
            self.visit(node.slice)
            self.opcodes[''] += '䛄'

    def visit_For(self, node):
        self.opcodes[''] += '鏡'
        self.visit(node.iter)
        self.opcodes[''] += '電'
        self.visit(node.target)
        self.opcodes[''] += '怏'
        for stmt in node.body:
            self.visit(stmt)
        self.opcodes[''] += '槓'

    def visit_Tuple(self, node):
        self.opcodes[''] += '夨'
        for a in node.elts:
            self.visit(a)
            self.opcodes[''] += '𠦪'
        if self.opcodes[''][-1] == "𠦪":
            self.opcodes[''] = self.opcodes[''][:-1]
        self.opcodes[''] += '𩰗'

    def visit_List(self, node):
        self.opcodes[''] += '滍'
        for a in node.elts:
            self.visit(a)
            self.opcodes[''] += '篍'
        if self.opcodes[''][-1] == "篍":
            self.opcodes[''] = self.opcodes[''][:-1]
        self.opcodes[''] += '笘'

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Not):
            self.opcodes[''] += '幭'
        elif isinstance(node.op, ast.USub):
            self.opcodes[''] += '幏'
        elif isinstance(node.op, ast.Invert):
            self.opcodes[''] += '冘'
        else:
            raise
        self.visit(node.operand)
        self.opcodes[''] += '𨟙'

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):
            self.opcodes[''] += '椁'
        elif isinstance(node.op, ast.Sub):
            self.opcodes[''] += '瓅'
        elif isinstance(node.op, ast.Mod):
            self.opcodes[''] += '陊'
        elif isinstance(node.op, ast.Mult):
            self.opcodes[''] += '黹'
        else:
            raise

        left = self.visit(node.left)
        self.opcodes[''] += '𠧞'
        right = self.visit(node.right)
        self.opcodes[''] += '㰟'

    def visit_Attribute(self, node):
        self.opcodes[''] += '𣢰'
        self.visit(node.value)
        self.opcodes[''] += '𠬢'
        self.opcodes[''] += node.attr
        self.opcodes[''] += '𢑌'

    def visit_BoolOp(self, node):
        for i in range(len(node.values) - 1):
            if isinstance(node.op, ast.And):
                self.opcodes[''] += '㳷'
            elif isinstance(node.op, ast.Or):
                self.opcodes[''] += '𦅻'
            else:
                raise

        self.visit(node.values[0])
        for value in node.values[1:]:
            self.opcodes[''] += '脼'
            self.visit(value)

def main():
    data = interpreter.getdump()
    with open('allresult.py', 'r', encoding="utf-8") as f:
        code = f.read()
    code = re.sub(r"# Import header start\n.*?# Import header end\n", "", code, flags=re.DOTALL)
    code = re.sub(r"# Var header start\n.*?# Var header end\n", "", code, flags=re.DOTALL)
    compiler = Compiler(data)
    instructions = compiler.compile(code)
    print(instructions)

if __name__ == "__main__":
    main()




