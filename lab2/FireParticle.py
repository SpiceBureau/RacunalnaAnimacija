import random
import pygame

class FireParticle: 
    def __init__(self, display, startingX, startingY) -> None:
        self.startingX = startingX
        self.startingY = startingY
        self.speed = 0
        self.acc = random.gauss(0.05, 0.01)
        self.x = startingX
        self.y = startingY
        self.display = display

        self.framesToLive = random.gauss(80, 20) # Gaussova distribucija sa očekivanjem μ = 90 i varijancijom μ = 30 za određivanje vremena života čestice

        particleSize = (random.gauss(8, 2), random.gauss(8, 2))
        try: self.s = pygame.Surface(particleSize, pygame.SRCALPHA)   
        except: print(particleSize)
        self.s.fill((255,0,0,128))                         
        display.blit(self.s, (self.startingX,self.startingY))
    
    def move(self, display, barrelX, barrelY, wind):
        self.framesToLive -= 1   
        if self.framesToLive < 0: self.reset(barrelX, barrelY)  # Ako 

        self.speed = self.speed + self.acc

        self.set_Color_and_Opacity(self.s)        

        if random.random() < 0.5: self.x = self.x + 3
        else: self.x = self.x - 3

        self.processWind(wind)

        self.y = self.y - self.speed            
        display.blit(self.s, (self.x,self.y))
    
    def set_Color_and_Opacity(self,s):
        greenPart = 180 - self.framesToLive*2.5
        if greenPart > 255: greenPart = 255
        elif greenPart < 0: greenPart = 0

        alpha = 100 + self.framesToLive
        if alpha > 255: alpha = 255
        elif alpha < 0: alpha = 0
        
        try: s.fill((255, greenPart, 0, alpha))            
        except ValueError: 
            print(self.framesToLive)
            quit()

    def reset(self, barrelX, barrelY):
        self.x = random.gauss(barrelX, 25)
        self.y = random.gauss(barrelY, 15)
        self.framesToLive = random.gauss(90, 30)
        self.speed = 0
    
    def setStartingCoord(self, x, y):
        self.startingX = x
        self.startingY = y
        
    def processWind(self, wind):
        if wind == 0: return

        heightNormalized = self.y / 900 
        if heightNormalized > 0.9: self.x = self.x + 0.25*wind
        elif heightNormalized < 0.9 and heightNormalized > 0.8: self.x = self.x + 1*wind
        elif heightNormalized < 0.8 and heightNormalized > 0.6: self.x = self.x + 2*wind
        elif heightNormalized < 0.6 and heightNormalized > 0.4: self.x = self.x + 4*wind
        elif heightNormalized < 0.4 and heightNormalized > 0.1: self.x = self.x + 8*wind
        elif heightNormalized < 0.1: self.x = self.x + 10*wind