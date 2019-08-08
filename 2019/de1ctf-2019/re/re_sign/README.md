# Re_Sign


1. `v = base64 (input)`

2. `check (v) => [(base64charset.index(char) + 1) for x in v] == res` 

> base64 的表可由调试得出，输入字符串调试结果与标准base64 结果比较可得表。

```python
import base64

cset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

# table_ 由调试得出
table_ = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 
'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 0, 'V', 'B', 'N', 'M', 'q', 'w', 'e', 'r', 0, 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 0, 0, '=']

# 有一部分缺失，这里只是猜测
# ['C', 't', '+', '/']
fake_table = []
for x in cset:
    if x not in table_:
        fake_table.append(x)
print(fake_table)

off = 0
for i in range(len(table_)):
    if table_[i] == 0:
        table_[i] = fake_table[off]
        off += 1

res = [8, 59, 1, 32, 7, 52, 9, 31, 24, 36, 19, 3, 16, 56, 9, 27, 8, 52, 19, 2, 8, 34, 18, 3, 5, 6, 18, 3, 15, 34, 18, 23, 8, 1, 41, 34, 6, 36, 50, 36, 15, 31, 43, 36, 3, 21, 65, 65]
b64flag = ''
for i in res:
    b64flag += cset[i - 1]
print(b64flag)
# H6AfGzIeXjSCP3IaHzSBHhRCEFRCOhRWHAohFjxjOeqjCU==

rawb64 = ''
for i in range(0x30):
    rawb64 += cset[table_.index(b64flag[i])]
print(rawb64)
# ZGUxY3Rme0VfTDRuZ3VhZzNfMXNfSzNLZUszX040Smk0fQ==

print(base64.b64decode(rawb64.encode()))
```