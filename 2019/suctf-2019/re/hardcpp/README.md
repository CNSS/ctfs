# hardCpp

控制流平坦化，要求输入刚好21位（包含一位回车）

**deflat** 然后爆破

```python=
import string
def re2():
    flag = ['f'] * 20
    dst = [243, 46, 24, 54, 225, 76, 34, 209, 249, 140, 64, 118, 244, 14, 0, 5, 163, 144, 14, 165]
    i = 1
    for each in dst:
        for x in string.printable:
            x = ord(x)
            if 0xff&(((ord(flag[i-1]) % 7) + x) ^ (((ord(flag[i-1]) ^ 18)*3)+2)) == each:
                flag[i] = chr(x)
                i += 1
                break
    flag = ''.join(flag)
    print(flag)
if __name__ == '__main__':
    re2()
```