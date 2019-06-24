We found two methods to solve it,

## use overflow
This is the eaiser way by using overflow in unit test.
The vulnerability is in systemKTest(sub_2ad8) function. If len(input) == 128, it will override part of systemKey to zero. Use this overflow with systemCheck(sub_2f6c) function, so we can override key to all zero in 5 rounds.

Finally send 0 as key to get shell.
You can found code of this part in function exp_overflow.

## use aes attack
We found system test is an eaiser version of [0ctf2016-people's-square](https://github.com/p4-team/ctf/tree/master/2016-03-12-0ctf/peoples_square)
By sending following sample and collect cipher
00 00 00 00 00 ... 00
01 00 00 00 00 ... 00
02 00 00 00 00 ... 00
03 00 00 00 00 ... 00
04 00 00 00 00 ... 00
..
FE 00 00 00 00 ... 00
FF 00 00 00 00 ... 00

We can calculate the key then get shell.
You can found code of this part in function exp_aes.