from enum import Enum
from heapq import *
from math import inf
from golf import parseGolf

class GolfBall:
    def __init__(self, position=[0, 0], velocity=[0, 0]):
        self.position = position
        self.velocity = velocity


class GolfGraph:
    def __init__(self, grid, ball, maxHits=7):
        self.grid = grid
        self.ball = ball
        self.path = [ball.position]
        self.numHits = 0
        self.totalEnergySpent = 0
        self.visited = set()

    class Position:
        def __init__(self, r, c):
            self.row = r
            self.col = c
            self.height = grid[r][c]

    # Determines where the player can hit the ball from its current position
    # TODO: Simplify this code!!!!!!!!!!
    def findAvailablePositions(self, row_init, col_init):
        # row_init, col_init = self.ball.position

        # print(row, col)
        height_init = grid[row_init][col_init]
        available_new_positions = []

        # TODO: Refactor into manageable pieces

        # UP Direction
        if row_init > 0:
            for i in range(row_init - 1, -1, -1):
                # TODO: Double check that there will be no logical errors
                #  if loop is exited when visited position is found
                if (i, col_init) in self.visited:
                    break

                height_current = grid[i][col_init]

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
        if row_init < len(grid) - 1:
            for i in range(row_init + 1, len(grid)):
                if (i, col_init) in self.visited:
                    break

                height_current = grid[i][col_init]

                # We have found the horizon
                if height_current > height_init:
                    # The horizon is adjacent to our initial position
                    if abs(row_init - i) == 1:
                        available_new_positions.append((i, col_init))
                    else:
                        # Aim for the position just before the horizon
                        available_new_positions.append((i - 1, col_init))
                    break

                if i == len(grid) - 1:
                    available_new_positions.append((i, col_init))
                    break

        # LEFT Direction
        if col_init > 0:
            for i in range(col_init - 1, -1, -1):
                if (row_init, i) in self.visited:
                    continue

                height_current = grid[row_init][i]

                # We have found the horizon
                if height_current > height_init:
                    # The horizon is adjacent to our initial position
                    if abs(col_init - i) == 1:
                        available_new_positions.append(("Left", row_init, i))
                    else:
                        # Aim for the position just before the horizon
                        available_new_positions.append(("Left", row_init, i + 1))
                    break

                if i == 0:
                    available_new_positions.append(("Left", row_init, i))
                    break

        # RIGHT Direction
        if col_init < len(grid[0]) - 1:
            for i in range(col_init + 1, len(grid[0])):
                if (row_init, i) in self.visited:
                    continue

                height_current = grid[row_init][i]

                # We have found the horizon
                if height_current > height_init:
                    # The horizon is adjacent to our initial position
                    if abs(col_init - i) == 1:
                        available_new_positions.append(("Right", row_init, i))
                    else:
                        # Aim for the position just before the horizon
                        available_new_positions.append(("Right", row_init, i - 1))
                    break

                if i == len(grid[0]) - 1:
                    available_new_positions.append(("Right", row_init, i))
                    break

        # for line in grid:
        #     print(line)
        return available_new_positions


    # Selection portion of greedy algorithm
    # Uses the information visible to ReMBot at its current poisiton to
    # TODO: Implement greedy algorithm to select position from available
    #  based on weighted criteria
    # TODO: Implement base case to stop when bottom-right corner is found
    def makeMove(self):
        pass

    def weight(self, cur_row, cur_col, neighbor_row, neighbor_col):
        pass

    # We treat the grid as a weighted digraph
    # The weight for the connection between adjacent positions
    # is assigned using a special function that takes in the difference in height (see weight above)
    def dijkstra(self):

        # Create a grid for the upper bounds of weighted distance estimates
        rows = len(grid)
        cols = len(grid[0])
        dist = [[inf] * cols for i in range(rows)]

        # Set the start position weighted distance as zero
        cur_row, cur_col = self.ball.position
        dist[cur_row][cur_col] = 0

        minh = [(0,0,0)]

        while not(len(minh) == 0):
            current = heappop(minh)
            neighbors = self.findAvailablePositions()



if __name__ == "__main__":
    grid = parseGolf.readFileIntoArray('sampleGrid1.txt')
    print(len(grid), len(grid[0]))
    print()
    positions_to_test = [[0,0], [3,0], [2,3], [3,4], [1,0], [1,1], [2,1]]
    '''for position in positions_to_test:
        ball = GolfBall(position=position)
        graph = GolfGraph(grid, ball)
        print(position)
        print(graph.findPaths())
        print()'''

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ball = GolfBall(position=[i,j])
            graph = GolfGraph(grid, ball)
            print(ball.position)
            print(graph.findAvailablePositions(ball.position[0], ball.position[1]))
            print()
    # print(grid)

    # newBall = ball + Direction.LEFT
    # print(newBall.position)

