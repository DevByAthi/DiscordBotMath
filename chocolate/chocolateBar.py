'''
This function assumes no merges are allowed, only breaks
'''

import numpy as np
from chocolate import factoring

# PRECONDITION: The width w and height h are whole numbers
#			    representing the dimensions of the given chocolate bar
# PRECONDITION: The desired area, m, is a whole number such that m <= w*h
def breakBar(width, height, desired_area, collectionSpace):

    # If no space left in collection, stop
    if (collectionSpace == 0):
        return -1

    # Redefined for simplicity in code
    w = width
    h = height
    m = desired_area

    # Check that preconditions are met
    if (min(m, w, h) < 1 or m > w * h):
        print("INVALID INPUTS")
        return -1

    '''
	Edge cases covered here (e.g. m equals area of chocolate bar)
	'''

    # Check if m equals the area of the original chocolate bar!
    if m == w * h:
        # print out bar
        return 0

    # Check if m can be factored into two numbers, m_1 and m_2, such that
    # max(m_1,m_2) <= min(w,h)
    # If this is not possible, return -1 and state IMPOSSIBLE

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
