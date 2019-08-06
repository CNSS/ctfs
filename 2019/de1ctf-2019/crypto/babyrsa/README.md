# De1taCTF-crypto-babyrsa
---
The raw problems can be found in "task.py". 
Our code can be found in "solve.py". 
You should read them first becouse most steps' solutions are explicitly illustrated in them except the final step. 
The details about final step are illustrated here.
$$
e = a*b \\
c^{bd} {\equiv} m^{abbd} {\equiv} m^b \bmod n\\
$$
So we can get a congruence equation.
$$
c_1^{14d_1} {\equiv} m^14 \bmod p \\
c_1^{14d_1} {\equiv} m^14 \bmod q_1\\
c_2^{14d_2} {\equiv} m^14 \bmod q_2
$$
Solve it, we can get a solution M.
Then follow the steps below, we can get the plaintext.
$$
M {\equiv} (m^2)^7 \bmod (q_1q_2)\\
d' = inv(7, q_1q_2)\\
m^2 {\equiv} M^{d'} \bmod (q_1q_2)
$$




