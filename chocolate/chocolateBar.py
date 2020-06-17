'''
This function assumes no merges are allowed, only breaks
'''

from math import gcd
import numpy as np
from chocolate import factoring

# PRECONDITION: The width w and height h are whole numbers
#			    representing the dimensions of the given chocolate bar
# PRECONDITION: The desired area, m, is a whole number such that m <= w*h
def breakBar(width, height, desired_area, spaceLeft=1):

    # If no space left in collection, stop
    if (spaceLeft == 0):
        return -1

    # Redefined for simplicity in code
    w = width
    h = height
    m = desired_area

    # Check that preconditions are met
    if (min(m, w, h) < 1 or m > w * h):
        return -1

    '''
	Edge cases covered here (e.g. m equals area of chocolate bar)
	'''

    # Check if m equals the area of the original chocolate bar!
    # This checks for a zero-break case
    if m == w * h:
        return 0

    # Check if m can be achieved by splitting chocolate bar in two
    # This checks for a one-break case
    denominator = gcd(w*h, m)
    if denominator == w or denominator == h:
        return 1

    # Find factors of m that fit in given chocolate bar
    factors_list = factoring.factorPairs(m)
    factors_list = [(a,b) for (a,b) in factors_list ]

    '''
    End of edge cases
    '''

    # Define the number of breaks as 0 initially

    # Factor m into m_1 and m_2. Let m_2 be the larger of the two factors
    '''
    Let L be the larger dimension between the width and the height of the chocolate bar
    Let l be the smaller dimension between the width and the height of the chocolate bar
    
    If m_2 is not equal to the length along dimension L
    	add 1 to the number of breaks
    	Print out the original chocolate bar with a dashed line after the m_2'th piece along dimension L
	If m_1 is not equal to the length along dimension l
		add 1 to the number of breaks
		Print out the original chocolate bar with a dashed line after the m_1'th piece along dimension L
	'''


# return number of breaks


# POSTCONDITION: Return a whole number representing the minimum number 
# of breaks needed to obtain desired area from the original chocolate bar, OR...
# "IMPOSSIBLE" if the desired area cannot be obtained


'''
'''


def breakBarWithMerge(width, height, desired_area):
    # Redefined for simplicity in code
    w = width
    h = height
    m = desired_area

    # Check that preconditions are met
    if (min(m, w, h) < 1) or (m > w * h):
        print("INVALID INPUTS")
        return -1

    # Check if any merges are truly needed
    initialBreak = breakBar(width, height, desired_area)
    if (initialBreak != -1):
        return initialBreak

# Otherwise,


if __name__ == "__main__":
    print("HI")
