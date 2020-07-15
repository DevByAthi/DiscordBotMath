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
        self.path = []
        self.numHits = 0
        self.totalEnergySpent = 0
        self.visited = set()

    # Determines where the player can hit the ball from its current position
    def findPaths(self):
        row, col = self.ball.position


    # Selection portion of greedy algorithm
    # Uses the information visible to ReMBot at its current poisiton to
    def makeMove(self):
        pass


if __name__ == "__main__":
    grid = parseGolf.readFileIntoArray('sampleGrid1.txt')
    ball = GolfBall(position=[5,10])
    graph = GolfGraph(grid, ball)

    newBall = ball + Direction.LEFT
    print(newBall.position)

