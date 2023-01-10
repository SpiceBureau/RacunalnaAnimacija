import random
import pygame
from FireParticle import FireParticle

class Barrel:
    def __init__(self, display, startingX, startingY) -> None:
        self.startingX = startingX
        self.startingY = startingY
        self.speed = 0
        self.acc = 0.1635
        self.x = startingX
        self.y = startingY
        self.display = display
        
        self.image = pygame.image.load('barrel.png')
        self.image = pygame.transform.scale(self.image, (25, 37))
        display.blit(self.image, (self.startingX,self.startingY))

        self.fireFlag = False
        self.fire = []

    def exist(self, display, wind):
        # Gravity
        if self.y < 880:
            self.speed = self.speed + self.acc
            self.y = self.y + self.speed
        else:
            self.speed = - self.speed / 2
            if self.speed < 0.5 and self.speed > -0.5: self.speed = 0
            else:
                self.speed = self.speed + self.acc
                self.y = self.y + self.speed
            if self.speed != 0:
                self.fireFlag = True # Ignite on ground contact


        display.blit(self.image, (self.x,self.y))

        if self.fireFlag:
            self.startFire(display)
            self.fireFlag = False
        if len(self.fire) != 0:
            for fp in self.fire:
                fp.move(display, self.x, self.y, wind)

    def startFire(self, display):
        for i in range(0, 400):
            xCoord = random.gauss(self.x, 9)
            yCoord = random.gauss(self.y, 10)
            self.fire.append(FireParticle(display, xCoord, yCoord))

        for i in range(0, 400):
            xCoord = random.gauss(self.x + 150, 9)
            yCoord = random.gauss(self.y, 10)
            self.fire.append(FireParticle(display, xCoord, yCoord))

    