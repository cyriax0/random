

from fractions import gcd
i=3
bignum = 2
s = 2
goal = 10
while i < goal:
    if gcd(bignum,i) == 1:
        print("prime:",i)
        bignum *= i
        s += i
    i += 2
print("Sum:",s)
    
