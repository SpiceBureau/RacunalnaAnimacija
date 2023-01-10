import math
import random
from time import sleep
import pygame, sys, numpy as np
from Points import Points
from pygame.locals import *
from Ant import Ant
from collections import Counter
from CentralBase import CentralBase

def main():
    pygame.init()

    WIDTH = 1300
    HEIGTH = 1000
    DISPLAY=pygame.display.set_mode((WIDTH,HEIGTH),0,32)

    clock = pygame.time.Clock()
    points = Points(n=20,r=45, width=WIDTH, height=HEIGTH)
    pointsDict = {}
    for point in points.points:
        pointsDict[point.getId()] = point
    
    centralBase = CentralBase()
    centralBase.setPoints(points)
    centralBase.setPointsDict(pointsDict)
    print("-"*40)
    while True:
        DISPLAY.fill((0, 0, 0))
        clock.tick(150)

        centralBase.handleKeys()
        centralBase.drawStuff(DISPLAY)
        pygame.display.update()
main()