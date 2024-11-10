#!/usr/bin/env python3
import json
import re
import interpreter

class IDX():
    def __init__(self, obj, key):
        self.obj = obj
        self.key = key

class FuluFunction():
    def __init__(self, data):
        self.name = data.name
        self.body = data.body
        self.variables = data.variables
        #self.name = data['name']
        #self.body = data['body']
        #self.variables = data['variables']
        self.code = ""
        self.tab = 1
        self.args = 0
        self.pc = 0
        self.stop = False
        self.result = None
    def Run(self, arg1=None, arg2=None, arg3=None):
        if (arg3 != None and self.args < 3) or (arg2 != None and self.args < 2) or (arg1 != None and self.args < 1):
            exit(1)
        self.arg1, self.arg2, self.arg3 = arg1, arg2, arg3
        self.appendcode(f'def {self.name}(arg1, arg2, arg3):\n')
        self.appendcode('# Var header start\n')
        for vhash in self.variables:
            try:
                self.appendcode(f'{"    " * self.tab}_{vhash[:8]} = {json.dumps(self.variables[vhash], ensure_ascii=False)}\n')
            except:
                self.appendcode(f'{"    " * self.tab}_{vhash[:8]} = {self.variables[vhash].__name__}\n')
        self.appendcode('# Var header end\n')
        while self.pc < len(self.body) and not self.stop:
            self.appendcode(f'{"    " * self.tab}')
            result = self._visit(self.body[self.pc:])
            self.appendcode('\n')
                
    def appendcode(self, code):
        self.code += code
        #print(code, end='')

    def _visitelts(self, x):
        self._visit(x)
        self.appendcode(', ')
    
    def _visitaddstr(self, x):
        self._visit(x)
        self.appendcode(' + ')

    def _visit(self, buf):
        if buf == None or len(buf) == 0:
            return
        op = buf[0]
        if op == "若":
            end = buf.find("喱") 
            new_pc = self.pc + end + 1
            self._print(buf[1:end])
            self.pc = new_pc
        elif op == '拑':
            level = 0
            end = 0
            for i in range(1,len(buf)): 
                if buf[i] == "趹":
                    if level == 0:
                        end = i
                        break
                    else:
                        level -= 1
                if buf[i] == "拑":
                    level += 1
            self._call(buf[1:end])
        elif op == '肖':
            self.pc += 1
            self.appendcode(f'arg1')
        elif op == '余':
            self.pc += 1
            self.appendcode(f'arg2')
        elif op == '槐':
            self.pc += 1
            self.appendcode(f'arg3')
        elif op == '䊆':
            self.pc += 129
            vhash = buf[1:129]
            if vhash not in self.variables:
                self.variables[vhash] = None
            self.appendcode(f'_{vhash[:8]}')
        elif op == "飧":
            level = 0
            end = 0
            for i in range(1,len(buf)): 
                if buf[i] == "婬":
                    if level == 0:
                        end = i
                        break
                    else:
                        level -= 1
                if buf[i] == "飧":
                    level += 1
            new_pc = self.pc + end + 1
            self.pc += 1
            self._if(buf[1:end])
            self.pc = new_pc
        elif op == "𧢼":
            self.pc += 1
            prev_pc = self.pc
            self.appendcode('(')
            self._visit(buf[1:])
            self.appendcode(' == ')
            next_pos = buf.find('盭') + 1 
            self._visit(buf[next_pos:])
            self.appendcode(')')
        elif op == "㸹":
            self.pc += 1
            prev_pc = self.pc
            self.appendcode('(')
            self._visit(buf[1:])
            self.appendcode(' not in ')
            next_pos = buf.find('盭') + 1
            self._visit(buf[next_pos:])
            self.appendcode(')')
        elif op == "㠭":
            self.pc += 1
            prev_pc = self.pc
            self.appendcode('(')
            self._visit(buf[1:])
            self.appendcode(' > ')
            next_pos = buf.find('盭') + 1
            self._visit(buf[next_pos:])
            self.appendcode(')')
        elif op == "漦":
            self.pc += 1
            prev_pc = self.pc
            self.appendcode('(')
            self._visit(buf[1:])
            self.appendcode(' >= ')
            next_pos = buf.find('盭') + 1
            self._visit(buf[next_pos:])
            self.appendcode(')')
        elif op == "𥄉":
            self.pc += 1
            prev_pc = self.pc
            self.appendcode('(')
            self._visit(buf[1:])
            self.appendcode(' <= ')
            next_pos = buf.find('盭') + 1
            self._visit(buf[next_pos:])
            self.appendcode(')')
        elif op == "𥄕":
            self.pc += 1
            prev_pc = self.pc
            self.appendcode('(')
            self._visit(buf[1:])
            self.appendcode(' != ')
            next_pos = buf.find('盭') + 1
            self._visit(buf[next_pos:])
            self.appendcode(')')
        elif op == "䔃":
            end = buf.find("陲")
            try:
                if buf.startswith("䔃腓"):
                    self.appendcode(f'{int(buf[2:end])}')
                elif buf.startswith("䔃拋"):
                    self.appendcode(f'{float(buf[2:end])}')
                elif buf.startswith("䔃𤞞"):
                    self.appendcode(json.dumps(buf[2:end], ensure_ascii=False))
                elif buf.startswith("䔃蛶"):
                    self.appendcode(f'{bool(buf[2:end] == "True")}')
                elif buf.startswith("䔃尥"):
                    self.appendcode(f'{bytes.fromhex(buf[2:end])}')
                elif buf.startswith("䔃𢏗陲"):
                    self.appendcode(f'None')
            except:
                if buf.startswith("䔃腓"):
                    self.appendcode(f'int({json.dumps(buf[2:end], ensure_ascii=False)})')
                elif buf.startswith("䔃拋"):
                    self.appendcode(f'float({json.dumps(buf[2:end], ensure_ascii=False)})')
                elif buf.startswith("䔃𤞞"):
                    self.appendcode(json.dumps(buf[2:end], ensure_ascii=False))
                elif buf.startswith("䔃蛶"):
                    self.appendcode(f'bool({json.dumps(buf[2:end], ensure_ascii=False)} == "True")')
                elif buf.startswith("䔃尥"):
                    self.appendcode(f'bytes.fromhex({json.dumps(buf[2:end], ensure_ascii=False)})')
                elif buf.startswith("䔃𢏗陲"):
                    self.appendcode(f'None')
        elif op == '狋':
            split = buf.find("竺") 
            end = buf.find("川") 
            split_pc = self.pc + split+1
            end_pc = self.pc+end+1
            self.pc += 1
            self._visit(buf[1:split])
            self.pc = split_pc
            self.appendcode(' = ')
            self._visit(buf[split+1:end])
            self.pc = end_pc
        elif op == '䫶':
            #self.appendcode(f'\n{"    " * self.tab}{{\n')
            #self.tab += 1
            self.appendcode('return ')
            result = self._visit(buf[1:])
            self.stop = True
            #self.tab -= 1
            #self.appendcode(f'\n{"    " * self.tab}}}\n')
            self.result = result
        elif op == '嵞':
            obj_end_pos = buf.find('慇')
            lower_end = buf.find('𦝠')
            upper_end = buf.find('騢')
            new_pc_0 = self.pc + obj_end_pos + 1
            new_pc_1 = self.pc + lower_end + 1
            new_pc_2 = self.pc + upper_end + 1
            
            obj = self._visit(buf[1:obj_end_pos])
            self.pc = new_pc_0
            self.appendcode('[')
            self._visit(buf[obj_end_pos+1: lower_end])
            self.pc = new_pc_1
            self.appendcode(':')
            self._visit(buf[lower_end+1:upper_end])
            self.pc = new_pc_2
            self.appendcode(']')
        elif op == "鏡":
            iter_pos = buf.find("電") 
            target_pos = buf.find("怏")
            body_pos = buf.find("槓")
            new_pc_0 = self.pc + iter_pos + 1
            new_pc_1 = self.pc + target_pos + 1
            new_pc_2 = self.pc + body_pos + 1
            
            tmpcode = self.code
            self.code = ''
            self._visit(buf[1:iter_pos])
            iterstr = self.code
            self.pc = new_pc_0
            self.code = ''
            self._visit(buf[iter_pos+1:target_pos])
            targetstr = self.code
            self.pc = new_pc_1
            self.code = tmpcode
            self.appendcode(f'for {targetstr} in {iterstr}:\n')
            self.tab += 1
            init_pc = self.pc
            block_size = body_pos - target_pos
            delta = self.pc - init_pc
            use = False
            while delta < block_size-1 and not self.stop:
                self.appendcode(f'{"    " * self.tab}')
                self._visit(buf[target_pos+1+delta:body_pos])
                self.appendcode('\n')
                delta = self.pc - init_pc
                use = True
            if not use:
                self.appendcode(f'{"    " * self.tab}pass\n')
            self.code = self.code[:-1]
            self.stop = False
            self.pc = new_pc_1
            self.tab -= 1
            #self.appendcode(f'{"    " * self.tab}}}')
            
            self.pc = new_pc_2
        elif op == "誋":
            pos = buf.find('𦵹')
            end = buf.find("䛄")
            new_pc_0 = self.pc + pos + 1
            new_pc_1 = self.pc + end + 1
            self._visit(buf[1:pos])
            self.pc = new_pc_0
            self.appendcode('[')
            self._visit(buf[pos+1: end])
            self.pc = new_pc_1
            self.appendcode(']')
        elif op == "夨":
            end = buf.find('𩰗')
            new_pc = self.pc + end + 1
            self.appendcode('(')
            elts = list(map(self._visitelts,filter(lambda x: x != "",buf[1:end].split('𠦪'))))
            if len(elts) > 0:
                self.code = self.code[:-2]
            self.appendcode(')')
            self.pc = new_pc
        elif op == "滍":
            end = buf.find('笘')
            new_pc = self.pc + end + 1
            self.appendcode('[')
            elts = list(map(self._visitelts,filter(lambda x: x != "",buf[1:end].split('篍'))))
            if len(elts) > 0:
                self.code = self.code[:-2]
            self.appendcode(']')
            self.pc = new_pc
        elif op == '幭':
            end = buf.find("𨟙")
            new_pc = self.pc + end + 1
            self.appendcode('(not ')
            self._visit(buf[1:end])
            self.appendcode(')')
            self.pc = new_pc
        elif op == '幏':
            end = buf.find("𨟙")
            new_pc = self.pc + end + 1
            self.appendcode('(-')
            self._visit(buf[1:end])
            self.appendcode(')')
            self.pc = new_pc
        elif op == '冘':
            end = buf.find("𨟙")
            new_pc = self.pc + end + 1
            self.appendcode('(~')
            self._visit(buf[1:end])
            self.appendcode(')')
            self.pc = new_pc
        elif op == '椁':
            end = buf.find("㰟")
            new_pc = self.pc + end + 1
            a, b = buf[1:end].split("𠧞")
            self.appendcode('(')
            self._visit(a)
            self.appendcode(' + ')
            self._visit(b)
            self.appendcode(')')
            self.pc = new_pc
        elif op == '瓅':
            end = buf.find("㰟")
            new_pc = self.pc + end + 1
            a, b = buf[1:end].split("𠧞")
            self.appendcode('(')
            self._visit(a)
            self.appendcode(' - ')
            self._visit(b)
            self.appendcode(')')
            self.pc = new_pc
        elif op == '陊':
            end = buf.find("㰟")
            new_pc = self.pc + end + 1
            a, b = buf[1:end].split("𠧞")
            self.appendcode('(')
            self._visit(a)
            self.appendcode(' % ')
            self._visit(b)
            self.appendcode(')')
            self.pc = new_pc
        elif op == '黹':
            end = buf.find("㰟")
            new_pc = self.pc + end + 1
            a, b = buf[1:end].split("𠧞")
            self.appendcode('(')
            self._visit(a)
            self.appendcode(' * ')
            self._visit(b)
            self.appendcode(')')
            self.pc = new_pc
        elif op == '𣢰':
            end = buf.find('𢑌')
            new_pc = self.pc + end + 1
            a,b = buf[1:end].split("𠬢")
            #self.appendcode('(')
            self._visit(a)
            #self.appendcode(f').({b})')
            self.appendcode(f'.{b}')
            self.pc = new_pc
        elif op == '㳷':
            self.appendcode('(')
            first = self._visit(buf[1:])
            self.appendcode(' and ')
            next_pos = buf.find('脼') + 1 
            self._visit(buf[next_pos:])
            self.appendcode(')')
        elif op == '𦅻':
            self.appendcode('(')
            self._visit(buf[1:])
            self.appendcode(' or ')
            next_pos = buf.find('脼') + 1 
            self._visit(buf[next_pos:])
            self.appendcode(')')
        else:
            self.appendcode('exit()')
            self.pc += 1
            #exit(1)
    def _print(self, buf):
        st = []
        format_head = 0
        format_end = 0
        while (format_head := buf.find("瀳", format_head)) != -1:
            st.append(buf[format_end:format_head])
            format_end = buf.find("適", format_head)
            st.append(buf[format_head+1:format_end])
            format_head = format_end
            format_end += 1
        if format_end != len(buf):
            st.append(buf[format_end:])
        self.appendcode('print(')
        #content = ''.join(list(map(lambda x: str(self._visit(x)),st)))
        content = list(map(self._visitaddstr,st))
        if len(content) > 0:
            self.code = self.code[:-3]
            self.appendcode(', ')
        self.appendcode('flush=True)')
    def _call(self, buf):
        final_pc = self.pc + len(buf)+2
        split_pos = buf.find("韔")
        args = list(map(lambda x: x if x!="" else None, buf[:split_pos].split("塺")))
        func_name = buf[split_pos+1:]
        result = [None, None]
        if '巜' in func_name:
            vs = func_name.split('巜')
            self._visit(vs[-1])
            for v in vs[:-1][::-1]:
                self.appendcode(f'.{v}')
        else:
            self.appendcode(f'{func_name}')
            
        self.appendcode('(')
        argstmp = list(filter(lambda x: x != None,map(self._visitelts,args)))
        if len(args) > 0:
            self.code = self.code[:-2]
        args = argstmp
        self.appendcode(')')
        self.pc = final_pc
    def _if(self, buf):
        condition_end = buf.find("嗔")
        if_branch = condition_end + 1
        level = 0
        else_branch = 0
        for i in range(condition_end+1,len(buf)): 
            if buf[i] == "𪊨":
                if level == 0:
                    else_branch = i
                    break
                else:
                    level -= 1
            if buf[i] == "嗔":
                level += 1
        
        #self.appendcode(f'{"    " * self.tab}condition = {{\n')
        #self.tab += 1
        self.appendcode('if ')
        self._visit(buf[:condition_end])
        #self.tab -= 1
        #self.appendcode(f'{"    " * self.tab}}}\n')
        #if self._visit(buf[:condition_end])[0]:
        self.appendcode(':\n')
        self.tab += 1
        self.pc += if_branch
        init_pc = self.pc
        block_size = else_branch - if_branch
        delta = self.pc - init_pc
        use = False
        while delta < block_size and not self.stop:
            self.appendcode(f'{"    " * self.tab}')
            self._visit(buf[if_branch+delta:else_branch])
            self.appendcode('\n')
            delta = self.pc - init_pc
            use = True
        if not use:
            self.appendcode(f'{"    " * self.tab}pass\n')
        self.stop = False
        self.tab -= 1
        #self.appendcode(f'{"    " * self.tab}}}\n')
        #else:
        self.appendcode(f'{"    " * self.tab}else:\n')
        self.tab += 1
        self.pc = init_pc + else_branch
        init_pc = self.pc
        block_size = len(buf) - else_branch -1
        delta = self.pc - init_pc
        use = False
        while delta < block_size and not self.stop:
            self.appendcode(f'{"    " * self.tab}')
            self._visit(buf[else_branch+1+delta:])
            self.appendcode('\n')
            delta = self.pc - init_pc
            use = True
        if not use:
            self.appendcode(f'{"    " * self.tab}pass\n')
        self.code = self.code[:-1]
        self.stop = False
        self.tab -= 1
        #self.appendcode(f'{"    " * self.tab}}}')

def main():
    #with open('dump_all.json', 'r', encoding="utf-8") as f:
    #    data = json.loads(f.read())
    data = interpreter.getdump()
    fulus = {}
    with open(f"allresult.py", 'w') as f:
        f.write("""# Import header start
import sys
import hashlib
import base64
import json
import os
import hmac
import hashlib
from db import connect
import random
import re
import time
from urllib.parse import urlparse, parse_qs
# Import header end

""")
        funcnamelist = list(data.keys())
        funcnamelist.sort()
        for a in funcnamelist:
            #fulus[data[a]['name']] = FuluFunction(data[a])
            fulus[data[a].name] = FuluFunction(data[a])
            print(f"{data[a].name}")
            try:
                #fulus[data[a]['name']].Run()
                fulus[data[a].name].Run()
            finally:
                f.write(fulus[data[a].name].code)
                f.write('\n')
                #print(fulus[data[a]['name']].code)
                #with open(f"{data[a].name}.asm", 'w') as f:
                #    f.write(fulus[data[a].name].code)
    #print(fulus)

if __name__ == "__main__":
    main()
