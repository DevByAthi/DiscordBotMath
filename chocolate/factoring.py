'''
Code for finding all pairs of factors for a given number, n. That is to say, all x,y such that n = x*y.
'''

def factorPairs(n):
    i = 2
    original = n
    pair_list = [(1, n)]
    while i**2 < original:
        if n % i == 0:
            pair_list.append((i, n//i))
        i += 1
    return pair_list

# For testing purposes
if __name__ == "__main__":
    print(factorPairs(50050))
