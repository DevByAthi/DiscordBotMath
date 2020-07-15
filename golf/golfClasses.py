from enum import Enum
from golf import parseGolf

class Direction(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    LEFT = (0,-1)
    RIGHT = (0,1)


class GolfBall:
    def __init__(self, position=[0, 0], velocity=[0, 0]):
        self.position = position
        self.velocity = velocity

    def __add__(self, other : Direction):
        new_row = self.position[0] + other.value[0]
        new_col = self.position[1] + other.value[1]
        return GolfBall(position=[new_row, new_col])


class GolfGraph:
    def __init__(self, grid, ball, maxHits=7):
        self.grid = grid
        self.ball = ball
        self.path = [ball.position]
        self.numHits = 0
        self.totalEnergySpent = 0
        self.visited = set()

    # Determines where the player can hit the ball from its current position
    def findPaths(self):
        row_init, col_init = self.ball.position
        # print(row, col)
        current_height = grid[row_init][col_init]
        available_new_positions = []
        # print("    ")
        # TODO: Allow this to be iterable over Directions Enum
        # UP direction
        cur_direction = Direction.DOWN
        # TODO: Have short-circuit evaluation if we are at the boundary
        #  and can't go in cur_direction
        flag = False
        bound, increment, init_point = self.selectBound(cur_direction, row_init, col_init)
        for i in range(init_point + increment, bound, increment):
            # print(i, grid[i][col])
            flag = self.atHorizon(row_init,col_init, i, col_init, increment, available_new_positions)
            # A horizon was found before reaching the edge of grid
            if (flag):
                break
            # No horizon was found and edge was reached
            elif i == bound - 1:
                available_new_positions.append([i, col_init])

        # for line in grid:
        #     print(line)
        return available_new_positions

    def __edgePosition(self, direction, row_init, col_init):
        d = {
            Direction.UP: (0, col_init),
            Direction.DOWN: (len(grid) - 1, col_init),
            Direction.LEFT: (row_init, 0),
            Direction.RIGHT: (row_init, len(grid[0]) - 1)
        }
        return d[direction]

    def selectBound(self, direction, row_init, col_init):
        d = {
            Direction.UP : (-1, -1, row_init),
            Direction.DOWN : (len(grid), 1, row_init),
            Direction.LEFT : (-1, -1, col_init),
            Direction.RIGHT : (len(grid[0]), 1, col_init)
        }
        return d[direction]

    def findHorizon(self):
        pass

    def atHorizon(self, row_init, col_init, row, col, increment, available_new_positions):
        horizon_found = False
        # if there is an unvisited position that has a greater height,
        # set this as the horizon for this direction
        if grid[row][col] > grid[row_init][col_init] and self.notYetVisited((row, col)):
            # If horizon is adjacent to current position, explore this position
            if abs(row_init - row) == 1 or abs(col_init - col) == 1:
                available_new_positions.append([row, col])
            # Otherwise, explore the position preceding horizon
            else:
                available_new_positions.append([row - increment, col])
            horizon_found = True

        # This horizon position within view has now been visited
        self.visited.add((row, col))
        return horizon_found

    def atBoundary(self, row, col, direction):
        if direction == Direction.UP or direction == Direction.DOWN:
            return not(0 < row < (len(grid) - 1))
        elif direction == Direction.LEFT or direction == Direction.RIGHT:
            return not(0 < col < (len(grid[0]) - 1))

    def notYetVisited(self, pos):
        return not(pos in self.visited)


    # Selection portion of greedy algorithm
    # Uses the information visible to ReMBot at its current poisiton to
    # TODO: Implement greedy algorithm to select position from available
    #  based on weighted criteria
    # TODO: Implement base case to stop when bottom-right corner is found
    def makeMove(self):
        pass


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
            print(graph.findPaths())
            print()
    # print(grid)

    # newBall = ball + Direction.LEFT
    # print(newBall.position)

