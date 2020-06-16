'''
Python code that implements Pollard's rho algorithm to find factor of a given number n
'''

import random as rand
from math import gcd, sqrt, floor, ceil

# For use in Pollard's Rho Algorithm
def f(x, n):
    return (x ** 2 - 1) % n

# TODO: Implement Pollard's Rho Algorithm
def pollardRho(n, factorSet):
    x = rand.random() * n
    y = f(x, n)
    factor = gcd(abs(x - y), n)

    while (factor == 1):
        x = f(x, n)


def naivePrimeFactorization(n):
    factor_list = []
    original = n

    for i in range(2, n):
        if i ** 2 >= n:
            break

        while n % i == 0:
            n /= i
            factor_list.append(i)

    if n > 1:
        factor_list.append(int(n))
    return factor_list

if __name__ == "__main__":
    factors_n = naivePrimeFactorization(500)
    print(factors_n)
