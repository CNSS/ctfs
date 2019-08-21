table_raw = "0123456789-abcdef"
table = 'ABCDEFGHIJ-123456'

dst = [74, 50, 50, 54, 49, 67, 54, 51, 45, 51, 73, 50, 73, 45, 69, 71, 69, 52, 45, 73, 66, 67, 67, 45, 73, 69, 52, 49, 65, 53, 73, 53, 70, 52, 72, 66]

res = ''
for x in dst:
    res += table_raw[table.index(chr(x))]
print("flag{" + res + "}")
