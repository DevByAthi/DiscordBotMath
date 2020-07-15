from golf import parseGolf


class GolfBall:
    def __init__(self, position=(0, 0), velocity=(0, 0)):
        self.position = position
        self.velocity = velocity


class GolfGraph:
    def __init__(self, grid, ball, maxHits=7):
        self.grid = grid
        self.ball = ball
        self.path = []
        self.numHits = 0
        self.totalEnergySpent = 0

    def findPaths(self):
        pass

    def makeMove(self):
        pass


if __name__ == "__main__":
    grid = parseGolf.readFileIntoArray('sampleGrid1.txt')
    ball = GolfBall()
    graph = GolfGraph(grid, ball)

