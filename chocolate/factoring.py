'''
Code for finding all pairs of factors for a given number, n. That is to say, all x,y such that n = x*y.
'''

from functools import reduce

def naivePrimeFactorization(n):
    factor_list = []

    for i in range(2, n):
        if i ** 2 >= n:
            break

        while n % i == 0:
            n /= i
            factor_list.append(i)

    if n > 1:
        factor_list.append(int(n))
    return factor_list

def factorPairs(n):
    factor_list = naivePrimeFactorization(n)
    pair_list = [(1, n)]
    for i in range(1, len(factor_list)):
        fac_1 = factor_list[0] if len(factor_list[:i]) == 1 else reduce(lambda x, y: x*y, factor_list[:i])
        fac_2 = factor_list[-1] if len(factor_list[i:]) == 1 else reduce(lambda x, y: x*y, factor_list[i:])
        pair_list.append((fac_1, fac_2))
    return pair_list


if __name__ == "__main__":
    factors_n = naivePrimeFactorization(500000)
    print(factors_n)
    print(factorPairs(50000))
