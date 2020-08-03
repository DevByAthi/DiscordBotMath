from enum import Enum
from heapq import *
from math import inf

import parseTopLevel
from golf import parseGolf


class GolfGraph:
    def __init__(self, grid):
        self.grid = grid
        self.path = []
        self.visited = set()

    # Determines where the player can hit the ball from its current position
    def findAvailablePositions(self, row_init, col_init):
        # row_init, col_init = self.ball.position

        # print(row, col)
        height_init = self.grid[row_init][col_init]
        available_new_positions = []

        # UP Direction
        if row_init > 0:
            for i in range(row_init - 1, -1, -1):

                height_current = self.grid[i][col_init]

                # We have found the horizon
                if height_current > height_init:
                    # The horizon is adjacent to our initial position
                    if abs(row_init - i) == 1:
                        available_new_positions.append((i, col_init))
                    else:
                        # Aim for the position just before the horizon
                        available_new_positions.append((i + 1, col_init))
                    break

                if i == 0:
                    available_new_positions.append((i, col_init))
                    break

        # DOWN Direction
        if row_init < len(self.grid) - 1:
            for i in range(row_init + 1, len(self.grid)):

                height_current = self.grid[i][col_init]

                # We have found the horizon
                if height_current > height_init:
                    # The horizon is adjacent to our initial position
                    if abs(row_init - i) == 1:
                        available_new_positions.append((i, col_init))
                    else:
                        # Aim for the position just before the horizon
                        available_new_positions.append((i - 1, col_init))
                    break

                if i == len(self.grid) - 1:
                    available_new_positions.append((i, col_init))
                    break

        # LEFT Direction
        if col_init > 0:
            for i in range(col_init - 1, -1, -1):

                height_current = self.grid[row_init][i]

                # We have found the horizon
                if height_current > height_init:
                    # The horizon is adjacent to our initial position
                    if abs(col_init - i) == 1:
                        available_new_positions.append((row_init, i))
                    else:
                        # Aim for the position just before the horizon
                        available_new_positions.append((row_init, i + 1))
                    break

                if i == 0:
                    available_new_positions.append((row_init, i))
                    break

        # RIGHT Direction
        if col_init < len(self.grid[0]) - 1:
            for i in range(col_init + 1, len(self.grid[0])):

                height_current = self.grid[row_init][i]

                # We have found the horizon
                if height_current > height_init:
                    # The horizon is adjacent to our initial position
                    if abs(col_init - i) == 1:
                        available_new_positions.append((row_init, i))
                    else:
                        # Aim for the position just before the horizon
                        available_new_positions.append((row_init, i - 1))
                    break

                if i == len(self.grid[0]) - 1:
                    available_new_positions.append((row_init, i))
                    break

        return available_new_positions

    # Compute the weight for the edge connecting two adjacent positions
    # Since the height difference between the two positions can be negative,
    # and since Dijkstra's algorithm and UCS require nonnegative weights,
    # a map is made from all integer to the nonnegative reals
    def weight(self, cur_row, cur_col, neighbor_row, neighbor_col):
        height_diff = self.grid[neighbor_row][neighbor_col] - self.grid[cur_row][cur_col]

        # This strange case is to ensure that we don't prefer
        # going on flat ground to going downhill
        if height_diff == 0:
            return 0.9

        if height_diff < 0:
            height_diff = pow(abs(height_diff) + 1, -1)
        return height_diff

    # An admissible heuristic, guaranteed to be less than
    # or equal to the sum of weights along the optimal path
    def heuristic(self, cur_row, cur_col):
        return pow(self.grid[cur_row][cur_col] + 1, -1)

    # We convert the grid into a weighted digraph
    # The weight for the connection between adjacent positions is assigned
    # using a special function that takes in the difference in height (see weight above)
    # INTENT: Find the optimal path from the start to the end assuming simplifying physical constraints
    # PRECONDITION: self.grid is a non empty 2D list representing a rectangular grid
    # PRECONDITION: start position is at (0,0), corresponding to the top-left corner of self.grid
    # PRECONDITION: goal position is at (len(self.grid) - 1, len(self.grid[0]) - 1) the bottom right corner of self.grid
    # PRECONDITION: all values in self.grid are nonnegative integers
    def a_star_greedy(self):

        # ==== Start of Pre-processing stage ====

        rows = len(self.grid)
        cols = len(self.grid[0])

        # Create a nested list for the upper bounds of weighted distance estimates
        # Default upper bound of a weighted distance is set to positive infinity
        # This will prove crucial to our greedy approach, as well as defining the states of the algorithm
        dist = [[inf] * cols for i in range(rows)]

        # Create a map for the predecessor of a position
        # That is, where the ball must travel from, starting from the top-left,
        # to reach a position while accruing the lowest total weight
        # This will be crucial to identifying the shortest path to the goal
        prev = {}

        # Set the start position weighted distance as zero
        dist[0][0] = 0

        # Start position has no predecessor
        prev[(0, 0)] = None

        # Min-heap used to order available positions by weight
        # The initial tuple stored is for the starting position, which is distance 0 away from the start
        minh = [(0.0, 0, 0)]

        self.visited.clear()

        # ==== End of Pre-processing stage ====

        while not (len(minh) == 0):

            # Retrieve position with lowest weighted distance
            current = heappop(minh)
            cur_weight, cur_row, cur_col = current

            # Mark current position as visited
            self.visited.add((cur_row, cur_col))

            # If the current node is the goal point, we are done! Return the path accumulated

            # Sc (complement): returnS is complete. In this context,
            # this means the list of upper bounds of weighted distances (dist)
            # allows us to find the shortest path to the goal has been found
            if self.atGoal(cur_row, cur_col):
                # print(prev)
                self.path = self.findPath(prev)
                self.path.reverse()
                return

            # Find neighbors of current position
            neighbors = self.findAvailablePositions(cur_row, cur_col)
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor

                # If this neighbor has already been visited,
                # it is not part of the frontier and can be ignored
                if (neighbor_row, neighbor_col) in self.visited:
                    continue

                # Calculate the weighted distance to neighboring position
                # This tuple will have a better upper bound on the distance to the associated position
                neighbor_weight = self.weight(cur_row, cur_col, neighbor_row, neighbor_col)

                # Decrease the upper bound on distance to this neighbor from the source as needed
                # Note that the weighted distance will include the weighted distance of the current position
                # This allows for the cumulative cost to be considered, as opposed to the immediate edge weight

                # Sa (Parts): the list of upper bounds of weighted distances (dist) contains part of the solution.
                # That is, updated upper bounds along the frontier contain
                # part of the weights of the shortest path fromthe start to the goal
                updated_bound = neighbor_weight + dist[cur_row][cur_col]
                if dist[neighbor_row][neighbor_col] > updated_bound:
                    # Include an admissible heuristic, which is just the ideal weight
                    # if the current position were directly connected to the goal

                    # [Sb (Greed Used)]: List of upper bounds of weighted distances has been updated
                    # to be closer to actual weighted distance
                    dist[neighbor_row][neighbor_col] = updated_bound + self.heuristic(cur_row, cur_col)

                    # Record the predecessor of this neighbor as current
                    prev[(neighbor_row, neighbor_col)] = (cur_row, cur_col)

                # Add the neighbor to the min-heap
                heappush(minh, (dist[neighbor_row][neighbor_col], neighbor_row, neighbor_col))

                # We've now visited this neighbor
                self.visited.add((neighbor_row, neighbor_col))

    # POSTCONDITION: The updated list self.path contains a sequence of tuples describing a path to the goal
    # POSTCONDITION: minh is not empty, else we would have found all
    # POSTCONDITION: (self.path)[0] = (0,0)
    # POSTCONDITION: (self.path)[-1] = (len(self.grid) - 1, len(self.grid[0]) - 1), the goal position

    # Checks if we have arrived at the bottom-right corner, our goal
    def atGoal(self, r, c):
        return r == len(self.grid) - 1 and c == len(self.grid[0]) - 1

    # This helper function updates the graph's path from the start to the goal,
    # using the dictionary generated by self.dijkstra()
    def findPath(self, prev):
        current_position = (len(self.grid) - 1, len(self.grid[0]) - 1)
        keys = prev.keys()
        path = []
        while current_position != (0, 0):
            if current_position not in keys:
                raise ValueError("Path not found to goal")
            path.append(current_position)
            current_position = prev[current_position]

        path.append(current_position)
        return path


if __name__ == "__main__":
    '''grid = parseGolf.readFileIntoArray('sampleGrid5.txt')
    # print(len(grid), len(grid[0]))

    # Test of findAvailablePositions
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ball = GolfBall(position=[i, j])
            graph = GolfGraph(grid, ball)
            print(ball.position)
            print(graph.findAvailablePositions(ball.position[0], ball.position[1]))
            print()'''

    num_files = 10

    for i in range(1, num_files + 1):
        file_name = "sampleGrid" + str(i) + ".txt"
        grid = parseGolf.readIntoGrid(parseTopLevel.readFileIntoString(file_name))
        print(file_name)
        print(len(grid), len(grid[0]))
        graph = GolfGraph(grid)
        graph.a_star_greedy()
        print(graph.path)
        print()
