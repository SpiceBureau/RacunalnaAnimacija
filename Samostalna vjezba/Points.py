import random
import string
import numpy as np
import matplotlib.pyplot as plt
from Point import Point

class Points():
    def __init__(self, n, r, width, height):
        self.n = n
        self.r = r
        self.width = width
        self.height = height

        self.points = []
        self.pointsToIterate = []
        self.createPoints()

        for point in self.pointsToIterate:
            point.getNeighbours(self.points)
    
    def createPoints(self):
        while len(self.points) < self.n:
            x = random.randint(45, self.width - 45)
            y = random.randint(45, self.height - 45)
            newPoint = Point(x, y, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))
            if len(self.points) == 0: 
                self.points.append(newPoint)
                self.pointsToIterate.append(newPoint)
                continue
            
            isToClose = False
            for point in self.points:
                if point.getDistanceBetweenPoints(newPoint) < self.r: isToClose = True

            if not isToClose: 
                self.points.append(newPoint)
                self.pointsToIterate.append(newPoint)


