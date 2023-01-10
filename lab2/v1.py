import random
import pygame, sys
from pygame.locals import *
from FireParticle import FireParticle
from barrel import Barrel
def main():
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('cambriacambriamath', 50)
    windText = my_font.render('Wind', False, (255, 255, 255))
    windSpeedText = my_font.render('Speed: 0 km/h', False, (255, 255, 255))
    windDirectionText = my_font.render('Direction: No wind', False, (255, 255, 255))

    pygame.event.set_allowed([QUIT, MOUSEBUTTONUP, KEYDOWN])

    DISPLAY=pygame.display.set_mode((1200,900),0,32)

    clock = pygame.time.Clock()
    
    barrelFLag = False
    barrels = []

    rArrow = pygame.image.load("Rarrow.png")
    rArrow = pygame.transform.scale(rArrow, (30, 30))

    lArrow = pygame.image.load("Larrow.png")  
    lArrow = pygame.transform.scale(lArrow, (30, 30))

    DISPLAY.blit(rArrow, (0, 0))
    DISPLAY.blit(lArrow, (0, 40))
    lRect = lArrow.get_rect()  
    rRect = rArrow.get_rect()
    lRect.y = 40
    
    wind = 0
    while True:
        DISPLAY.fill((0, 0, 0))
        clock.tick(60)
        DISPLAY.blit(rArrow, (0, 0))
        DISPLAY.blit(lArrow, (0, 40))
        point = pygame.mouse.get_pos()
        rCollide = rRect.collidepoint(point)
        lCollide = lRect.collidepoint(point)
        #print(rCollide, lCollide)

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    barrels = []   # Očisti screen

            if event.type == MOUSEBUTTONUP:
                if event.button == 3: 
                    pos = pygame.mouse.get_pos()
                    barrels.append(Barrel(DISPLAY, pos[0], pos[1]))    # Stvori bačvu (izvor vatre)
                    barrelFLag = True

                elif event.button == 1:
                    if rCollide: 
                        wind += 1
                        windspeed = pow(2, abs(wind)) 
                        windSpeedText = my_font.render('Speed: {0} km/h'.format(windspeed if windspeed != 1 else 0), False, (255, 255, 255))
                        windDirectionText = my_font.render('Direction: {0}'.format("West" if windspeed != 1 else "No wind"), False, (255, 255, 255))
                    elif lCollide: 
                        wind += -1
                        windspeed  = pow(2, abs(wind)) 
                        windSpeedText = my_font.render('Speed: {0} km/h'.format(windspeed if windspeed != 1 else 0), False, (255, 255, 255))
                        windDirectionText = my_font.render('Direction: {0}'.format("East" if windspeed != 1 else "No wind"), False, (255, 255, 255))
        
        if barrelFLag: 
            for barrel in barrels:
                barrel.exist(DISPLAY, wind)
        DISPLAY.blit(windText, (890,15))
        DISPLAY.blit(windSpeedText, (890,50))
        DISPLAY.blit(windDirectionText, (890,85))
        pygame.display.update()
main()