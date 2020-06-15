'''
Python code that implements Pollard's rho algorithm to find factor of a given number N
'''

import random as rand
from math import gcd, sqrt

def f(x, N):
	return (x ** 2 - 1) % N;

def pollardRho(N, factorSet):

	x = rand.random() * N;
	y = f(x,N);
	factor = gcd(abs(x-y), N);

	while (factor == 1):
		x = f(x);


def naiveFactoring(N):
	factors = set();
	for i in range(sqrt(N)):
		if (N % i == 0):
			N /= i;
			factors.add(i);	