from numpy import random as np_random
import numpy as np
import matplotlib.pyplot as plt
import math 
import random
import pygame

class Point():
    def __init__(self, x, y, uniqueId):
        self.x = x
        self.isStartEnd = False
        self.y = y
        self.neighbours = {}
        self.trailsValues = {}
        self.numberOfConnections = random.choices([1, 2, 3, 4], weights=[1, 3, 4, 3], k=1)[0]
        self.color = [0, 0, 0]
        self.rect = pygame.Rect((x - 5, y - 5), (10, 10))
        self.uniqueId = uniqueId
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDistanceBetweenPoints(self, otherPoint):
        return math.dist([self.getX(), self.getY()], [otherPoint.getX(), otherPoint.getY()])
    
    def getNeighbours(self, points):
        distances = {}
        for point in points:
            if point.getId() == self.uniqueId: continue
            distances[point] = self.getDistanceBetweenPoints(point)
        while self.numberOfConnections > 0:
            if len(distances) == 0: return
            minKey = min(distances, key=distances.get)
            minDistance = distances[minKey]
            del distances[minKey]
            if minDistance > np_random.poisson(lam=200, size=1): return
            if minKey.numberOfConnections > 0: 
                self.neighbours[minKey] = 0
                self.numberOfConnections -= 1
                self.trailsValues[minKey.getId()] = 1

                minKey.neighbours[self] = 0
                minKey.numberOfConnections -= 1
                minKey.trailsValues[self.getId()] = 1
    
    def getTrailValues(self):
        return self.trailsValues
    def setTrailValues(self, trailValues):
        self.trailsValues = trailValues
    
    def getId(self):
        return self.uniqueId
    def setId(self, uniqueId):
        self.uniqueId = uniqueId

