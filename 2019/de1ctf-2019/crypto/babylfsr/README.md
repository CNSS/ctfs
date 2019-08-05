This is a very general challenge

You can use the **BM algorithm** to get the feedback polynomial [Berlekamp-Massey Algorithm](https://raw.githubusercontent.com/bozhu/BMA/master/bma.py)

The difficulty with this challenge is that using the BM algorithm requires a sequence of length 2 * n (256 * 2 in this case), and this problem only gives 504 bits, so you need brute force the 8 bits

Because the feedback polynomial has an x^1 to the first term, you can simply step back and get the initial state