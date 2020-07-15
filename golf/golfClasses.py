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
        row, col = self.ball.position
        print(row, col)
        current_height = grid[row][col]
        available_new_positions = []
        print("    ")

        # UP direction
        # TODO: Optimize this code
        # TODO: Repeat for other directions, extracting into separate function
        flag = False
        for i in range(row - 1, -1, -1):
            print(i, grid[i][col])
            # if there is an unvisited position that has a greater height,
            # set this as the horizon for this direction
            if grid[i][col] > current_height and self.notYetVisited((i,col)):
                # If horizon is adjacent to current position,
                # then mark this as the place you must explore
                if abs(row - i) == 1:
                    available_new_positions.append([i, col])
                # Otherwise, explore the position just before the horizon
                else:
                    available_new_positions.append([i + 1, col])
                flag = True
                break

        if not(flag):
            available_new_positions.append([0, col])

        return available_new_positions

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
    ball = GolfBall(position=[3,1])
    graph = GolfGraph(grid, ball)
    print(grid)
    print(len(grid), len(grid[0]))

    # newBall = ball + Direction.LEFT
    # print(newBall.position)
    print(graph.findPaths())

