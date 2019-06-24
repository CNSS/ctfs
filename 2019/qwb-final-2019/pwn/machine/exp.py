from pwn import *
from  hashlib import md5

context.log_level = 'debug'

def pass_pow(prefix, chash):
    sample_space = [chr(i) for i in range(256)]
    guess = ""
    for i in sample_space:
        for j in sample_space:
            for k in sample_space:
                if md5(prefix+i+j+k).hexdigest() == chash:
                    guess = ''.join([i, j, k])
                    break
    return guess

ciphertexts = []

sbox = (0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
        0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 
        0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 
        0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 
        0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 
        0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 
        0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 
        0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 
        0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 
        0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 
        0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 
        0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 
        0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 
        0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 
        0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 
        0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16)

invsbox = []
for i in range(256):
    invsbox.append(sbox.index(i))

def SubBytes(state):
    state = [list(c) for c in state]
    for i in range(len(state)):
        row = state[i]
        for j in range(len(row)):
            state[i][j] = sbox[state[i][j]]
    return state

def InvSubBytes(state):
    state = [list(c) for c in state]
    for i in range(len(state)):
        row = state[i]
        for j in range(len(row)):
            state[i][j] = invsbox[state[i][j]]
    return state

def rowsToCols(state):
    cols = []
    
    #convert from row representation to column representation
    cols.append([state[0][0], state[1][0], state[2][0], state[3][0]])
    cols.append([state[0][1], state[1][1], state[2][1], state[3][1]])
    cols.append([state[0][2], state[1][2], state[2][2], state[3][2]])
    cols.append([state[0][3], state[1][3], state[2][3], state[3][3]])
    
    return cols

def colsToRows(state):
    rows = []
    
    #convert from column representation to row representation 
    rows.append([state[0][0], state[1][0], state[2][0], state[3][0]])
    rows.append([state[0][1], state[1][1], state[2][1], state[3][1]])
    rows.append([state[0][2], state[1][2], state[2][2], state[3][2]])
    rows.append([state[0][3], state[1][3], state[2][3], state[3][3]])
    
    return rows

###########
# Key schedule functions
###########
# key schedule helper function
def RotWord(word):
    r = []
    r.append(word[1])
    r.append(word[2])
    r.append(word[3])
    r.append(word[0])
    return r

# key schedule helper function
def SubWord(word):
    r = []
    r.append(sbox[word[0]])
    r.append(sbox[word[1]])
    r.append(sbox[word[2]])
    r.append(sbox[word[3]])
    return r

# key schedule helper function
def XorWords(word1, word2):
    r = []
    for i in range(len(word1)):
        r.append(word1[i] ^ word2[i])
    return r

def printWord(word):
    str = ""
    for i in range(len(word)):
        str += "{0:02x}".format(word[i])
    print str

Rcon = [[0x01,0x00,0x00,0x00], [0x02,0x00,0x00,0x00], [0x04,0x00,0x00,0x00],
    [0x08,0x00,0x00,0x00], [0x10,0x00,0x00,0x00], [0x20,0x00,0x00,0x00], 
    [0x40,0x00,0x00,0x00], [0x80,0x00,0x00,0x00],[0x1B,0x00,0x00,0x00], 
    [0x36,0x00,0x00,0x00]]

# key is a 4*Nk list of bytes, w is a Nb*(Nr+1) list of words
# since we're doing 4 rounds of AES-128, this means that
# key is 16 bytes and w is 4*(4+1) words
def KeyExpansion(key):
    Nk = 4
    Nb = 4
    Nr = 4
    
    temp = [0,0,0,0]
    w=[]
    for i in range(Nb*(Nr+1)):
        w.append([0,0,0,0])
    
    i = 0
    
    #the first word is the master key
    while i<Nk:
        w[i] = [key[4*i],key[4*i+1], key[4*i+2], key[4*i+3]]
        
        #printWord(w[i])
        i = i+1
    
    i=Nk

    while i < (Nb*(Nr+1)):
        #print "Round ", i
        temp = w[i-1]
        #printWord(temp)
        if (i % Nk) == 0:

            temp = XorWords(SubWord(RotWord(temp)), Rcon[i/Nk-1])

        w[i] = XorWords(w[i-Nk], temp)
        i = i+ 1
        
    return w

def Shiftrows(state):
    state = colsToRows(state)

    #move 1
    state[1].append(state[1].pop(0))
    
    #move 2
    state[2].append(state[2].pop(0))
    state[2].append(state[2].pop(0))
    
    #move 3
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))
    
    return rowsToCols(state)   

def InvShiftrows(state):
    state = colsToRows(state)

    #move 1
    state[1].insert(0,state[1].pop())
    
    #move 2
    state[2].insert(0,state[2].pop())
    state[2].insert(0,state[2].pop())
    
    #move 3
    state[3].insert(0,state[3].pop())
    state[3].insert(0,state[3].pop())
    state[3].insert(0,state[3].pop())
    
    return rowsToCols(state)    

#converts integer x into a list of bits
#least significant bit is in index 0
def byteToBits(x):
    r = []
    while x>0:
        if (x%2):
            r.append(1)
        else:
            r.append(0)
        x = x>>1

    #the result should have 8 bits, so pad if necessary
    while len(r) < 8:
        r.append(0)
        
    return r

#inverse of byteToBits
def bitsToByte(x):
    r = 0
    for i in range(8):
        if x[i] == 1:
            r += 2**i
            
    return r

# Galois Multiplication
def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256

#single column multiplication
def mixColumn(column):
    temp = []
    for i in range(len(column)):
        temp.append(column[i])
    
    column[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ \
                galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
    column[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ \
                galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
    column[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ \
                galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
    column[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ \
                galoisMult(temp[1],1) ^ galoisMult(temp[0],3)    
    
    return column

def MixColumns(cols):
    #cols = rowsToCols(state)
    
    r = [0,0,0,0]
    for i in range(len(cols)):
        r[i] = mixColumn(cols[i])
    
    return r

def mixColumnInv(column):
    temp = []
    for i in range(len(column)):
        temp.append(column[i])
    
    column[0] = galoisMult(temp[0],0xE) ^ galoisMult(temp[3],0x9) ^ galoisMult(temp[2],0xD) ^ galoisMult(temp[1],0xB)
    column[1] = galoisMult(temp[1],0xE) ^ galoisMult(temp[0],0x9) ^ galoisMult(temp[3],0xD) ^ galoisMult(temp[2],0xB)
    column[2] = galoisMult(temp[2],0xE) ^ galoisMult(temp[1],0x9) ^ galoisMult(temp[0],0xD) ^ galoisMult(temp[3],0xB)
    column[3] = galoisMult(temp[3],0xE) ^ galoisMult(temp[2],0x9) ^ galoisMult(temp[1],0xD) ^ galoisMult(temp[0],0xB)    
                
    return column

def InvMixColumns(cols):
    #cols = rowsToCols(state)
    
    r = [0,0,0,0]
    for i in range(len(cols)):
        r[i] = mixColumnInv(cols[i])
    
    return r

#state s, key schedule ks, round r
def AddRoundKey(s,ks,r):

    for i in range(len(s)):
        for j in range(len(s[i])):
            s[i][j] = s[i][j] ^ ks[r*4+i][j]

    return s

########
# Encrypt functions
#########
# for rounds 1-3
def oneRound(s, ks, r):
    s = SubBytes(s)
    s = Shiftrows(s)
    s = MixColumns(s)
    s = AddRoundKey(s,ks,r)
    return s

def oneRoundDecrypt(s, ks, r):
    s = AddRoundKey(s,ks,r)
    s = InvMixColumns(s)
    s = InvShiftrows(s)
    s = InvSubBytes(s)
    return s

# round 4 (no MixColumn operation)
def finalRound(s, ks, r):
    s = SubBytes(s)
    s = Shiftrows(s)
    s = AddRoundKey(s,ks,r)
    return s

def finalRoundDecrypt(s, ks, r):
    s = AddRoundKey(s,ks,r)
    s = InvShiftrows(s)
    s = InvSubBytes(s)
    return s

# Put it all together
def encrypt4rounds(message, key):
    s = []
    
    #convert plaintext to state
    s.append(message[:4])
    s.append(message[4:8])
    s.append(message[8:12])
    s.append(message[12:16])
    
    #compute key schedule
    ks = KeyExpansion(key)
    
    #apply whitening key
    s = AddRoundKey(s,ks,0)
    
    c = oneRound(s, ks, 1)
    c = oneRound(c, ks, 2)
    c = oneRound(c, ks, 3)
    c = finalRound(c, ks, 4)
    
    #convert back to 1d list
    output = []
    for i in range(len(c)):
        for j in range(len(c[i])):
            output.append(c[i][j])
    
    return output

def swapRows(rows):
    result = []
    for i in range(4):
        for j in range(4):
            result.append(rows[j*4+i])
    return result

def decrypt4rounds(message, key):
    s = []
    
    #convert plaintext to state
    s.append(message[:4])
    s.append(message[4:8])
    s.append(message[8:12])
    s.append(message[12:16])
    
    #compute key schedule
    ks = KeyExpansion(key)
    
    #apply whitening key
    s = finalRoundDecrypt(s, ks, 4)
    
    c = oneRoundDecrypt(s, ks, 3)
    c = oneRoundDecrypt(c, ks, 2)
    c = oneRoundDecrypt(c, ks, 1)
    c = AddRoundKey(c,ks,0)

    #convert back to 1d list
    output = []
    for i in range(len(c)):
        for j in range(len(c[i])):
            output.append(c[i][j])
    
    return output

testCt = range(16)
testState = []
testState.append(testCt[:4])
testState.append(testCt[4:8])
testState.append(testCt[8:12])
testState.append(testCt[12:16])

key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 
        0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

ks = KeyExpansion(key)

textData = [0]*16
assert AddRoundKey(AddRoundKey(testState, ks, 1), ks, 1) == testState
assert InvMixColumns(MixColumns(testState)) == testState
assert InvShiftrows(Shiftrows(testState)) == testState
assert InvSubBytes(SubBytes(testState)) == testState
assert oneRoundDecrypt(oneRound(testState, ks, 1), ks, 1) == testState
assert finalRoundDecrypt(finalRound(testState, ks, 1), ks, 1) == testState
assert decrypt4rounds(encrypt4rounds(textData, key), key) == textData

#########################
# Attack code goes here #
#########################

def backup(ct, byteGuess, byteIndex):
    # We just need to check sums
    # There is no mixColumns in the last round, so skip it.
    # shiftRows just changes the byte's position. We don't care, so skip it.
    # All we need is a single xor for the guessed byte, and InvSubBytes

    t = ct[byteIndex] ^ byteGuess
    return invsbox[t]

def integrate(index):
    if len(ciphertexts) != 256:
        print "ERROR"
    potential = []

    for candidateByte in range(256):
        sum = 0
        for ciph in ciphertexts:
            oneRoundDecr = backup(ciph, candidateByte, index)
            sum ^= oneRoundDecr
        if sum == 0:
            potential.append(candidateByte)
    return potential

from itertools import product

def integral():
    candidates = []
    for i in range(16):
        candidates.append(integrate(i))
    print 'candidates', candidates
    for roundKey in product(*candidates):
        masterKey = round2master(roundKey)
        plain = ''.join(chr(c) for c in decrypt4rounds(ciphertexts[1], masterKey))
        if '\0\0\0\0' in plain:
            print 'solved', masterKey
            return masterKey

# Calculate the master key candidate from the final round key candidate
def round2master(rk):
    Nr=4
    Nk=4
    Nb=4
    w = []
    for i in range(Nb*(Nr+1)):
        w.append([0,0,0,0])
        
    i=0
    while i<Nk:
        w[i] = [rk[4*i],rk[4*i+1], rk[4*i+2], rk[4*i+3]]
        i = i+1

    j = Nk
    while j < Nb*(Nr+1):
        if (j%Nk) == 0:
            w[j][0] = w[j-Nk][0] ^ sbox[w[j-1][1] ^ w[j-2][1]] ^ Rcon[Nr - j/Nk][0]
            for i in range(1,4):
                w[j][i] = w[j-Nk][i] ^ sbox[w[j-1][(i+1) % 4] ^ w[j-2][(i+1) % 4]]
        else:
            w[j] = XorWords(w[j-Nk], w[j-Nk-1])
        j = j+1
    
    m = []
    for i in range(16,20):
        for j in range(4):
            m.append(w[i][j])

    return m
    
######################
# Printing functions #
######################
def printState(s):
    print "State:"
    for i in range(len(s)):
        row = s[i]
        rowstring = ""
        for j in range(len(row)):
            rowstring += "{0:02x} ".format(row[j])
        print rowstring
    print "\n"


def printKey(ks):
    for i in range(len(ks)):
        row = ks[i]
        rowstring = ""
        for j in range(len(row)):
            #rowstring += "{0:02x} ".format(row[j])
            rowstring += "{0:4} ".format(row[j])
        print rowstring
    print "\n"

def exp_aes(p):
    p.recvuntil('[+]Proof-Your-Heart:')
    prefix = p.recv(10).decode('hex')
    chash = p.recv(33)[1:]
    guess = pass_pow(prefix, chash)

    p.sendline(guess.encode('hex'))
    p.sendlineafter('[+]', '1')
    p.sendlineafter('[+]', '1')

    global ciphertexts
    for i in range(256):
        p.sendlineafter('[+]', '1')
        p.sendlineafter('[+]', '3')
        p.clean()
        p.sendline('%02x000000000000000000000000000000' % i)
        p.recvuntil('[+]')
        ret = p.recvline().strip()
        if len(ret) == 35:
            ret = ret[3:]
        assert len(ret) == 32
        ciphertexts.append(ret)
    ciphertexts = [[ord(c) for c in x.decode('hex')] for x in ciphertexts]
    p.sendlineafter('[+]', '1')
    p.sendlineafter('[+]', '2')
    sleep(0.1)
    secret = p.recv(35)[3:].decode('hex')
    key = integral()
    secret = [ord(c) for c in secret]
    secret = decrypt4rounds(secret, key)
    p.sendlineafter('[+]', '1')
    p.sendlineafter('[+]', '5')
    p.sendline(''.join(chr(c) for c in secret).encode('hex'))

def exp_overflow(p):
    p.recvuntil('[+]Proof-Your-Heart:')
    prefix = p.recv(10).decode('hex')
    chash = p.recv(33)[1:]
    guess = pass_pow(prefix, chash)

    p.sendline(guess.encode('hex'))
    p.sendlineafter('[+]', '2')
    p.sendlineafter('[+]', '1')
    for i in range(5):
        p.sendlineafter('[+]', '2')
        p.sendlineafter('[+]', '3')
        p.sendlineafter('[+]', 'a'*128)
        p.recv(3)
        p.sendlineafter('[+]', '2')
        p.sendlineafter('[+]', '6')
        p.recvuntil('[+]')
        p.recvuntil('[+]')
        p.recvuntil('[+]')
    p.sendlineafter('[+]', '2')
    p.sendlineafter('[+]', '5')
    p.recv(3)
    p.sendlineafter('[+]', '0'*128)
    
if __name__ == '__main__':
    p = process('./machine')
    exp_aes(p)
    # exp_overflow(p)
    p.interactive()