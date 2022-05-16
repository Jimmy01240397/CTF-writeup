# Magic
## 題目
![image](https://user-images.githubusercontent.com/57281249/168683836-1587fef8-00bd-4e75-9f46-ba4677fca419.png)

## Hint
![image](https://user-images.githubusercontent.com/57281249/168683883-eafbd557-d85a-4928-84df-fa4d2d7a42ef.png)

``` python
#!/usr/bin/python3

from pwn import *

context.arch = 'amd64'

elf = ELF('./magic')

got_write = elf.got['write']
got_read = elf.got['read']
plt_write = elf.plt['write']
plt_read = elf.plt['read']

read_hook_addr = 0x401d00
write_hook_addr = 0x401e00
preinit_func_addr = 0x401f00

bss = 0x404f00
rcnt_addr =  bss+0x0
wcnt_addr =  bss+0x8
real_read =  bss+0x10
real_write = bss+0x18
str1_addr =  bss+0x20
str2_addr =  bss+0x28

read_hook = asm(f"""
cmp rdx, 0xe
jne _0
push rax
push rdi
push rsi
push rdx
mov rax, 1
mov rdi, 1
mov rsi, {str1_addr}
mov rdx, 5
syscall
pop rdx
pop rsi
pop rdi
pop rax

_0:
mov rax, {rcnt_addr}
add qword ptr [rax], 1
mov rax, qword ptr [rax]

mov rbx, {wcnt_addr}
mov rbx, qword ptr [rbx]

mov r8, {real_read}
mov r8, qword ptr [r8]

cmp rax, 14
jne _1
cmp rbx, 8
jne _1

mov rdx, 0x1000
_1:
jmp r8
""")

write_hook = asm(f"""
push rax
push rdi
push rsi
push rdx
mov rax, 1
mov rdi, 1
mov rsi, {str2_addr}
mov rdx, 5
syscall
pop rdx
pop rsi
pop rdi
pop rax

mov rax, {wcnt_addr}
add qword ptr [rax], 1
mov rax, qword ptr [rax]

mov rbx, {rcnt_addr}
mov rbx, qword ptr [rbx]

mov r8, {real_write}
mov r8, qword ptr [r8]

cmp rax, 3
jne _1
cmp rbx, 7
jne _1

mov rdx, 0x100
_1:
jmp r8
""")

preinit_func = asm(f"""
mov r8, {str1_addr}
mov rax, 0xa776f656d
mov qword ptr [r8], rax

mov r8, {str2_addr}
mov rax, 0xa666f6f77
mov qword ptr [r8], rax

_0:
mov rdi, 0xffffffff
mov r8, {plt_read}
call r8
mov rax, {real_read}
mov r9, {got_read}
mov r9, qword ptr [r9]
mov qword ptr [rax], r9
mov rax, {got_read}
mov r9, {read_hook_addr}
mov qword ptr [rax], r9

mov rdi, 0xffffffff
mov r8, {plt_write}
call r8
mov rax, {real_write}
mov r9, {got_write}
mov r9, qword ptr [r9]
mov qword ptr [rax], r9
mov rax, {got_write}
mov r9, {write_hook_addr}
mov qword ptr [rax], r9
ret
""")

with open("./magic", "rb+") as f:
    rva = lambda x: x-0x400000
    data = list(f.read())
    data[rva(read_hook_addr):rva(read_hook_addr+len(read_hook))] = list(read_hook)
    data[rva(write_hook_addr):rva(write_hook_addr+len(write_hook))] = list(write_hook)
    data[rva(preinit_func_addr):rva(preinit_func_addr+len(preinit_func))] = list(preinit_func)
    f.seek(0)
    f.write(bytes(data))
```
