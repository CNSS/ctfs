import hashlib


class LFSR():
    def __init__(self, init, mask, length):
        self.init = init
        self.length = length
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    def next(self):
        nextdata = (self.init << 1) & self.lengthmask
        i = self.init & self.mask & self.lengthmask
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        nextdata ^= output
        self.init = nextdata
        return output

    def step_back(self):
        output = self.init & 1
        predata = self.init >> 1
        high_bit = parity(predata & self.mask) ^ output
        self.init = (high_bit << (self.length - 1)) | predata


def parity(x):
    res = 0
    while x:
        x -= x & (-x)
        res ^= 1
    return res


def Berlekamp_Massey_algorithm(sequence):
    N = len(sequence)
    s = sequence[:]

    for k in range(N):
        if s[k] == 1:
            break
    f = set([k + 1, 0])  # use a set to denote polynomial
    l = k + 1

    g = set([0])
    a = k
    b = 0

    for n in range(k + 1, N):
        d = 0
        for ele in f:
            d ^= s[ele + n - l]

        if d == 0:
            b += 1
        else:
            if 2 * l > n:
                f ^= set([a - b + ele for ele in g])
                b += 1
            else:
                temp = f.copy()
                f = set([b - a + ele for ele in f]) ^ g
                l = n + 1 - l
                g = temp
                a = b
                b = n - l + 1

    # output the polynomial
    def print_poly(polynomial):
        result = ''
        lis = sorted(polynomial, reverse=True)
        for i in lis:
            if i == 0:
                result += '1'
            else:
                result += 'x^%s' % str(i)

            if i != lis[-1]:
                result += ' + '

        return result

    return (print_poly(f), l)


def generate_mask(s, length):
    s = s.replace(' ', '')
    s = s.split('+')
    mask = 0
    for x in s:
        if 'x^' in x:
            e = int(x[2:])
            if e >= length:
                continue
            mask |= 1 << e
        elif x == '1':
            mask |= 1
    b = bin(mask)[2:].rjust(length, '0')
    return int(b[::-1], 2)


def bit_stream_to_int(a):
    return int(''.join(map(str, a)), 2)


def pad(m):
    pad_length = 8 - len(m)
    return pad_length*'0'+m


LENGTH = 256

for i in range(256):
    file = open("output", "r")
    data = file.read()
    file.close()
    result = []
    for j in range(len(data)):
        num = int(data[j], 2)
        result.append(num)
    tmp = pad(bin(i)[2:])
    for j in range(len(tmp)):
        num = int(tmp[j], 2)
        result.append(num)
    stream_z = tuple(result)
    eq, length = Berlekamp_Massey_algorithm(stream_z)
    # print("eq:", eq)
    # print("len:", length)
    if length != LENGTH:
        continue
    mask = generate_mask(eq, length)
    # print("mask:", bin(mask)[2:])
    stat = bit_stream_to_int(stream_z[:LENGTH])
    # print('stat:', bin(stat)[2:])

    if mask.bit_length() != LENGTH:
        continue
    # assert(stat.bit_length()==LENGTH)

    stream = LFSR(stat, mask, length)
    step_num = length
    for j in range(step_num):
        stream.step_back()
    res = stream.init
    for j in range(len(stream_z)):
        assert stream.next() == stream_z[length - step_num + j]

    # print("res:", bin(res)[2:])
    flag = "de1ctf{"+hashlib.sha256(hex(res)[2:].rstrip('L')).hexdigest()+"}"
    if flag[7:11] == '1224':
        print("flag:", flag)
        break
