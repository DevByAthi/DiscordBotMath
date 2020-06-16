'''
Python code that implements Pollard's rho algorithm to find factor of a given number n
'''

import random as rand
from math import gcd, sqrt, floor, ceil

factors = dict()

def f(x, n):
    return (x ** 2 - 1) % n


def pollardRho(n, factorSet):
    x = rand.random() * n
    y = f(x, n)
    factor = gcd(abs(x - y), n)

    while (factor == 1):
        x = f(x, n)


def naiveFactoring(n):
    factors_n = set()
    init_val = n
    for i in range(1, ceil(sqrt(init_val))):
        if n % i == 0:
            n /= i
            factors_n.add(i)
    return factors_n




if __name__ == "__main__":
    factors_n = naiveFactoring(10)
    print(factors_n)