
import pygame
from pygame.locals import *
import random
import math


class Ant():

    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.location = [startPoint.x, startPoint.y]
        self.targetPoint = None
        self.currentPoint = startPoint
        self.path = [startPoint.getId()]
        self.speed = random.randint(3,4)
        self.active = True
    
    def evaluatePath(self, byNumOfNodes, byDistance):
        if byNumOfNodes: return len(self.path)
    def setActiveStatus(self, status):
        self.active = status
    def getActiveStatus(self):
        return self.active