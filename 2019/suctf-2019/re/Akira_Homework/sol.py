
dst = [47, 31, 32, 46, 52, 4, 55, 45, 16, 57, 124, 34, 123, 117, 10, 56, 57, 33]
table = [1, 5, 4, 2, 3, 0]
passwd = [0] * 18
magic = [17, 69, 20, 73, 134, 100, 64, 80, 96, 193, 57, 45, 0, 0, 0, 0]

for i, x in enumerate(dst):
    i_idx = 6 * (i // 6) + table[i % 6]
    passwd[i_idx] = dst[i] ^ magic[1]
    passwd[i_idx] ^= i_idx

print(bytearray(passwd))
# passwd => Akira_aut0_ch3ss_!

import binascii, hashlib

dst = [-4, -82, -21, 110, 52, -76, 48, 62, -103, -71, 18, 6, -67, 50, 95, 43]

print(binascii.hexlify(bytearray([x & 0xff for x in dst])))

# Overwatch
print(hashlib.md5('Overwatch').hexdigest())

###########