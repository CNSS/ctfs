# flat

题目似乎对循环做了处理，但可以通过调试分析。

题目先对`flag`做了格式检验。
`formt_0` (`0400710`) 
![](https://i.imgur.com/Qfj3iFg.png)
`format_1` (`04008B0`)
![](https://i.imgur.com/T1ThaPd.png)
`format_2` (`0400980`)
![](https://i.imgur.com/juIkGAT.png)
![](https://i.imgur.com/00VWPPn.png)
![](https://i.imgur.com/iN864H2.png)
![](https://i.imgur.com/pB5F2e5.png)
得出 `flag` 格式： `flag{01234567-9012-4567-9012-456789012345}`

然后对 `flag` 进行处理，并与指定数据比较。调试发现加密函数是对数据逐字节处理，所以直接调试找出对应关系。
```python
table_raw = "0123456789-abcdef"
table = 'ABCDEFGHIJ-123456'

dst = [74, 50, 50, 54, 49, 67, 54, 51, 45, 51, 73, 50, 73, 45, 69, 71, 69, 52, 45, 73, 66, 67, 67, 45, 73, 69, 52, 49, 65, 53, 73, 53, 70, 52, 72, 66]

res = ''
for x in dst:
    res += table_raw[table.index(chr(x))]
print("flag{" + res + "}")
```
