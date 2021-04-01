#----------------------------------------------------
# Author: William Watkins
# Assignment: RSA CS378 hmwk-7
# Date: 4/23/2020
# This program implements components of RSA:
#   compute private and public keys, encrypt, decrypt
#----------------------------------------------------

from random import randint
from math import gcd

# low range 100-digit number
LOW = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# high range 101-digit number
HIGH = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000


def fermat(): #-----------------------------------fermat
    # return random large prime integer
    prime = False
    while prime == False:
        # generate random int between LOW and HIGH - 1
        r = randint(LOW, HIGH)
        
        #find a coprime
        coprime = False
        while coprime == False:
            # random int between 0 and r - 1
            a = randint(0, r)
            if gcd(a, r) == 1:
                # a, r are coprimes
                coprime = True
                
        # if a^(r-1) (mod r) = 1
        if modexp(a, r - 1, r) == 1:
            # r is prime
            prime = True
            
    return r

def modexp(x, y, n): #--------------------------------modexp
    # returns x^y (mod n)
    if y == 0:
        return 1
    z = modexp(x, y//2, n)
    
    # if y is even
    if y % 2 == 0:
        # return z^2 (mod n)
        return (z * z) % n
    else:
        # return x * z^2 (mod n)
        return (x * z * z) % n

def get_e(phi_n): #-----------------------------------get_e
    # return random int e where gcd(e, (p-1)(q-1)) = 1
    while True:
        for i in range(65537, HIGH):
            if gcd(i, phi_n) == 1:
                return i
        

def inverse(a, b): #----------------------------------inverse
    # return multiplicative inverse d = e^(-1) (mod(p-1)(q-1))
    # -> ax + by = 1 = gcd(a, b)
    t = 0
    newT = 1
    r = b
    newR = a
    
    while newR != 0:
        q = r // newR # quotient b/a
        t, newT = newT, t - q * newT
        r, newR = newR, r - q * newR
        
    if r > 1:
        return 1
    if t < 0:
        t = t + b
        
    return t
    


#-------------------------------------------------main

# p, q are large primes
# difference between p, q should be at least 10^95
diff = 0
while diff < (10 ** 95):
    p = fermat()
    q = fermat()
    diff = abs(p - q)
    
print('p = ', p)
print('q = ', q)

# n = pq
n = q * p
print('n = ', n)

# phi(n) = (p-1)(q-1)
phi_n = (p - 1) * (q - 1)

# find integer e such that gcd(e, (p-1)(q-1)) = 1
e = get_e(phi_n)
print('e = ', e)

# pair (n, e) is public key
# output to file public_key
with open('public_key', 'w') as f:
    f.write(str(n))
    f.write('\n')
    f.write(str(e))

# find multiplicitave inverse d = e^(-1) (mod (p-1)(q-1))
# d is private key
d = inverse(e, phi_n)
# output to file private_key
with open('private_key', 'w') as f:
    f.write(str(d))
# don't print -> d is secret

# encrypt message
with open('message', 'r') as f:
    m = f.read()

# c = ciphertext
c = modexp(int(m), e, n)

# output to file ciphertext
with open('ciphertext', 'w') as f:
    f.write(str(c))
print('c = ', c)

# decrypt
# m_orig = decrypted original message
m_orig = modexp(c, d, n)

# output to file decrypted_text
with open('decrypted_text', 'w') as f:
    f.write(str(m_orig))
print('original m = ', m_orig)
