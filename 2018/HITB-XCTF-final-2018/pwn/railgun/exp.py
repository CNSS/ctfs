from pwn import *
import os
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

pad = lambda x: x+(chr(16-len(x)) * (16-len(x)))

def aesecb_decrypt(enStr, key):
    cipher = AES.new(key, AES.MODE_ECB)
    enStr = pad(enStr)
    return cipher.decrypt(enStr)

def ex_gcd(m, n):
    x, y, x1, y1 = 0, 1, 1, 0
    while m % n:
        x, x1 = x1 - m // n * x, x
        y, y1 = y1 - m // n * y, y
        m, n = n, m % n
    return n, x, y

def mod_inv(x, p):
    g, y, k = ex_gcd(x, p)
    if y < p:
        y += p
    return y

def mining(p):
    p.recvuntil('[-]')
    p.sendline('2')
    p.recvuntil('mining:')
    sha256 = p.recvuntil('+', drop=True)
    s = p.recvuntil('\n', drop=True).decode('hex')
    for i in xrange(0x10000):
        if hashlib.sha256(s + p16(i)).hexdigest() == sha256:
            p.sendline(p16(i).encode('hex'))
            break

def get_pub(p):
    p.recvuntil('[-]')
    p.sendline('3')
    p.recvuntil('pub:')
    pub = p.recv(256)
    return int(pub, 16)

def get_flag_cipher(p):
    p.recvuntil('[-]')
    p.sendline('4')
    p.recvuntil('attack\n[+]')
    flagc = p.recv(256)
    return int(flagc, 16)

def shoot(p, boss_id, payload):
    p.recvuntil('[-]')
    p.sendline('5')
    p.recvuntil('boss:')
    p.sendline(str(boss_id))
    p.recvuntil('send:')
    p.sendline(payload)
    p.recvuntil('coins(1/0):')
    p.sendline('1')
    p.recvuntil('pickup:')
    cipher = p.recv(32)
    return cipher

def comment(p, len, payload):
    p.recvuntil('[-]')
    p.sendline('7')
    p.recvuntil('lenth:')
    p.sendline(str(len))
    p.recvuntil('comment:')
    p.send(payload)

def pwn(p):
    p.recvuntil('[+]PoW:')
    sha256 = p.recvuntil('+', drop=True)
    s = p.recvuntil('\n', drop=True).decode('hex')
    for i in xrange(0x10000):
        if hashlib.sha256(s + p16(i)).hexdigest() == sha256:
            p.sendline(p16(i).encode('hex'))
            break

    p.recvuntil('[-]description:')
    p.sendline('-')
    p.recvuntil('[-]name:')
    p.sendline('Kyr1os')

    e = 0x10001
    n1 = get_pub(p)
    inv16 = mod_inv(16, n1)
    flag_cipher = get_flag_cipher(p)

    mining(p)
    shoot(p, 1, '1'*256) # get 1 - 2 = 255 coins

    p.recvuntil('[-]')
    p.sendline('6') # accerate
    for i in range(10): # for remote
        comment(p, 18, '\x00'*18)
    x = 0
    Y = 1
    b = 0
    for round in range(200):
        drop = shoot(p, 9, hex(flag_cipher * Y)[2:].upper())
        half_byte = aesecb_decrypt(drop.decode('hex'), '\x00'*16)[0]
        half_byte = (int(half_byte, 16)+16-((b * pow(inv16, x, n1)) % n1 % 16)) % 16
        b += (half_byte * (16 ** x))
        x += 1
        y = pow(inv16, x, n1)
        Y = pow(y, e, n1)
    print hex(b)[2:].decode('hex') # flag

if __init__ == "__main__":
    # p = remote('192.168.17.12', 20002)
    p = process('./railgun')
    pwn(p)