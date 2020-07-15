class GolfBall:
    def __init__(self, position = (0,0), velocity = (0,0)):
        self.position = position
        self.velocity = velocity

class GolfGraph:
    def __init__(self, grid, ball):
        self.grid = grid
        self.path = []
        self.numHits = 0
        self.totalEnergySpent = 0
        self.ball = ball

    def findPaths(self):
        pass

    def makeMove(self):
        pass
