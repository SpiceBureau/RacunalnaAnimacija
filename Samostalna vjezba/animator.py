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
    points = Points(n=300,r=40, width=WIDTH, height=HEIGTH)
    
    centralBase = CentralBase()
    centralBase.setPoints(points)
    print("-"*40)
    while 1:
        DISPLAY.fill((200, 200, 200))
        clock.tick(220)

        centralBase.handleKeys()
        centralBase.drawStuff(DISPLAY)
        pygame.display.update()
main()