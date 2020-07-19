from enum import Enum
from heapq import *
from math import inf
from golf import parseGolf


class GolfGraph:
    def __init__(self, grid):
        self.grid = grid
        self.path = []
        self.visited = set()

    # Determines where the player can hit the ball from its current position
    # TODO: Simplify this code!!!!!!!!!!
    def findAvailablePositions(self, row_init, col_init):
        # row_init, col_init = self.ball.position

        # print(row, col)
        height_init = self.grid[row_init][col_init]
        available_new_positions = []

        # TODO: Refactor into manageable pieces

        # UP Direction
        if row_init > 0:
            for i in range(row_init - 1, -1, -1):
                # TODO: Double check that there will be no logical errors
                #  if loop is exited when visited position is found
                if (i, col_init) in self.visited:
                    break

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
                if (i, col_init) in self.visited:
                    break

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
                if (row_init, i) in self.visited:
                    continue

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
                if (row_init, i) in self.visited:
                    continue

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

        # for line in grid:
        #     print(line)
        return available_new_positions

    # Compute the weight for the edge connecting two adjacent positions
    # Since the height difference between the two positions can be negative,
    # and since Dijkstra's algorithm and UCS require nonnegative weights,
    # a map is made from all integer to the nonnegative reals
    def weight(self, cur_row, cur_col, neighbor_row, neighbor_col):
        height_diff = self.grid[neighbor_row][neighbor_col] - self.grid[cur_row][cur_col]

        # This strange case is dont to ensure that we don't prefer
        # going on flat ground to going downhill
        # TODO: Should this value be 0, meaning it is preferred to go flat over going downhill,
        #  or should if be > 0.5, meaning it is preferred to go downhill over flat?
        # Perhaps the heuristic can compensate...
        if height_diff == 0:
            return 0

        if height_diff < 0:
            height_diff = pow(abs(height_diff) + 1, -1)
        return height_diff

    # TODO: See if heuristic can incorporate Manhattan weighted distance into value,
    #  i.e. take minimum sum of weighted distance from current position to an edge
    #  with that from edge to goal
    # TODO: Verify that heuristic is admissible
    # TODO: Verify that heuristic is actually useful
    # TODO: Verify that heuristic makes function greedy
    def heuristic(self, cur_row, cur_col):
        return self.weight(cur_row, cur_col, len(self.grid) - 1, len(self.grid[0]) - 1)

    # We treat the grid as a weighted digraph
    # The weight for the connection between adjacent positions
    # is assigned using a special function that takes in the difference in height (see weight above)
    # TODO: Change from UCS to UCS with heuristic (greedy)
    def a_star_greedy(self):

        rows = len(self.grid)
        cols = len(self.grid[0])

        # Create a grid for the upper bounds of weighted distance estimates
        dist = [[inf] * cols for i in range(rows)]

        # Create a map for the predecessor of a position
        # That is, where the ball must travel from, starting from the top-left,
        # to reach a position
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

        while not (len(minh) == 0):
            # Retrieve position with lowest weighted distance
            current = heappop(minh)
            cur_weight, cur_row, cur_col = current
            # print(cur_row, cur_col, dist[cur_row][cur_col])

            # Mark current position as visited
            self.visited.add((cur_row, cur_col))

            # If the current node is the goal point, we are done! Return the path accumulated
            if self.atGoal(cur_row, cur_col):
                # print(prev)
                self.path = self.findPath(prev)
                self.path.reverse()
                return

            # Find neighbors of current position
            neighbors = self.findAvailablePositions(cur_row, cur_col)
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor

                # Calculate the weighted distance to neighboring position
                # This tuple will have a better upper bound on the distance to the associated position
                neighbor_weight = self.weight(cur_row, cur_col, neighbor_row, neighbor_col)

                # Decrease the upper bound on distance to this neighbor from the source as needed

                # Include an admissible heuristic, which is just the ideal weight
                # if the current position were directly connected to the goal

                # Note that the weighted distance will include the weighted distance of the current position
                # This allows for the cumulative cost to be considered, as opposed to the immediate edge weight
                updated_bound = neighbor_weight + dist[cur_row][cur_col] + self.heuristic(cur_row, cur_col)
                if dist[neighbor_row][neighbor_col] > updated_bound:
                    dist[neighbor_row][neighbor_col] = updated_bound
                    # Record the predecessor of this neighbor as current
                    prev[(neighbor_row, neighbor_col)] = (cur_row, cur_col)

                # Add the neighbor to the min-heap
                heappush(minh, (dist[neighbor_row][neighbor_col], neighbor_row, neighbor_col))

                # We can assume we haven't visited this neighbor, as this has been checked in findAvailablePositions()
                # TODO: Figure out if this affects the outcome, might be a logical bug
                self.visited.add((neighbor_row, neighbor_col))

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

    num_files = 9

    for i in range(1, num_files + 1):
        file_name = "sampleGrid" + str(i) + ".txt"
        grid = parseGolf.readIntoGrid(parseGolf.readFileIntoString(file_name))
        print(file_name)
        print(len(grid), len(grid[0]))
        graph = GolfGraph(grid)
        graph.a_star_greedy()
        print(graph.path)
        print()
