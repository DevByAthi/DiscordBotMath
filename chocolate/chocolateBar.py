'''
This function assumes no merges are allowed, only breaks
'''

from math import gcd
import numpy as np
from chocolate import factoring


# returns a dictionary with dimensions of one-break approximations of desired area for each dimension
def approximateOneBreaks(width, height, desired_area):
    return {
        "break_height-wise_width": width,
        "break_height-wise_height": (desired_area // width),
        "break_width-wise_width": (desired_area // height),
        "break_width-wise_height": height
    }

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

    # Check if m equals the area of the original chocolate bar!
    # This checks for a zero-break case
    if m == w * h:
        return 0

    # Check if m can be achieved by splitting chocolate bar in two
    # This checks for a one-break case
    denominator = gcd(w * h, m)
    if denominator == w or denominator == h:
        return 1

    # If the chocolate bar cannot be split once to yield desired area
    # We must make two consecutive breaks to yield a rectangle with the desired area

    # Find factors of m that fit in given chocolate bar
    factors_list = [(m_1, m_2) for (m_1, m_2) in factoring.factorPairs(m) if
                    (max(m_1, m_2) <= max(w, h)) and (min(m_1, m_2) <= min(w, h))]
    print(factors_list)  # DEBUG

    # No valid factor pairs could be found, so we must divide-and-conquer
    if len(factors_list) == 0:
        breakConstants = approximateOneBreaks(w, h, m)


# return number of breaks


# POSTCONDITION: Return a whole number representing the minimum number 
# of breaks needed to obtain desired area from the original chocolate bar, OR...
# "IMPOSSIBLE" if the desired area cannot be obtained


if __name__ == "__main__":
    print("HI")
    print(breakBar(3, 8, 13))
