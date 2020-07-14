import numpy as np

def getLongestSnakeSequence(a_grid):
    # Abstract: Return the longest snake sequence in the given grid, where a snake sequence is made up of adjacent
    # numbers in the grid such that for each number, the number on the right or below it is +1/-1 its value.
    #
    # Example:
    #   a_grid: 5 9 2 1 1
    #           4 5 6 7 9   has longest snake sequence (5, 4, 5, 6, 7, 8, 9)
    #           8 9 9 8 9
    #
    # Pre (input): a_grid is a rectangular 2-D numpy array of integers
    # Pre (dynamic): knownS is a set of solutions for a simpler sub-grid of a_grid
    # Post (dynamic): knownS contains a solution for the longest snake sequence in the entirety of a_grid
    # Post (output): The longest snake sequence has been returned as a list of integers

    # [Sa] (enough known): knownS includes enough solutions for sub-grids of a_grid to solve a_grid.
    # knownS shall be represented as an array with the same dimensions as a_grid. Each element of knownS is an integer
    # representing the length of the longest snake sequence ending at that position.
    knownS = np.zeros([a_grid.shape[0],a_grid.shape[1]])

    # We will iteratively approach [Sa] by starting at the top-left element, then checking each element to the right
    # and below the current element to see if it qualifies being added to the snake sequence.
    for i in range(knownS.shape[0]):
        for j in range(knownS.shape[1]):
            if (j < knownS.shape[1] - 1) and (abs(a_grid[i,j+1] - a_grid[i,j]) == 1):
                knownS[i,j+1] = knownS[i,j] + 1
            if (i < knownS.shape[0] - 1) and (abs(a_grid[i,j+1] - a_grid[i,j]) == 1):
                knownS[i+1,j] = knownS[i,j] + 1

    # Sb (output): longestSnakeSeq is a list of integers representing the longest snake sequence in a_grid and has been
    # returned. Once we've achieved Sa, the element with the highest value in knownS will be the head of the
    # longest snake sequence, so we simply have to trace it back to its tail. We can get the largest element's
    # coordinates with some help from numpy.
    crds = np.where(knownS == np.amax(knownS))
    crds = list(zip(crds[0],crds[1]))[0]
    x = crds[1]
    y = crds[0]
    longestSnakeSeq = [a_grid[y,x]]

    while knownS[y,x] != 0:
        if (y > 0) and (knownS[y-1,x] == knownS[y,x] - 1):
            y = y - 1
            longestSnakeSeq.insert(0,a_grid[y,x])
            continue
        if (x > 0) and (knownS[y,x-1] == knownS[y,x] - 1):
            x = x - 1
            longestSnakeSeq.insert(0,a_grid[y,x])
            continue

    return longestSnakeSeq

if __name__ == "__main__":
    # Testing
    print("Easier test.\nExpected: [1, 2, 3, 4]\nActual:")
    test_array_1 = np.array([[1,2,3], [3,4,4]])
    print(getLongestSnakeSequence(test_array_1))

    print("\nDifficult test.\nExpected: [9, 8, 7, 6, 5, 6, 7]\nActual:")
    test_array_2 = np.array([[9,6,5,2], [8,7,6,5], [7,3,1,6], [1,1,1,7]])
    print(getLongestSnakeSequence(test_array_2))
