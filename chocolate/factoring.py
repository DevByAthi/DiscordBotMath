'''
Python code that implements Pollard's rho algorithm to find factor of a given number n
'''

import random as rand
from math import gcd, sqrt, floor


def f(x, n):
    return (x ** 2 - 1) % n


def pollardRho(n, factorSet):
    x = rand.random() * n
    y = f(x, n)
    factor = gcd(abs(x - y), n)

    while (factor == 1):
        x = f(x, n)


def naiveFactoring(n):
    factors = set()
    for i in range(floor(sqrt(n))):
        if (n % i == 0):
            n /= i
            factors.add(i)


if __name__ == "__main__":
    print("TEST")
