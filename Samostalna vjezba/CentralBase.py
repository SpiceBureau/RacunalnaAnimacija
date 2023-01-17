

from collections import Counter
import math
import random
import sys
from time import sleep
from Ant import Ant
from Point import Point
from Points import Points
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np
import copy
import pygame


class CentralBase():

    def __init__(self):
        self.epoch = 0
        self.width = 1300
        self.height = 1000
        self.n = 250
        self.maxNodesAllowedToVisit = 150
        self.liveAnts = None
        self.startPoint = None
        self.endPoint = None
        self.points = None
        self.ants = []
        self.successfulAnts = []
        self.pointsDict = None
        self.linesColor = {}
        self.avgPathByEpoch = []
        self.successfulAntsByEpoch = []
        pass
    
    def setStartPoint(self, startPoint):
        self.startPoint = startPoint
    def getStartPoint(self):
        return self.startPoint
    def setEndPoint(self, endPoint):
        self.startPoint = endPoint
    def getEndPoint(self):
        return self.endPoint
    def setPoints(self, points):
        pointsDict = {}
        self.points = points
        self.linesColor = {}
        self.ants = []
        pointsAlreadyDoneForLines = []
        for point in self.points.points:
            trailValues = point.getTrailValues()
            for uniqueId, value in trailValues.items():
                if (point.getId(), uniqueId) in pointsAlreadyDoneForLines: continue
                self.linesColor[(point.getId(), uniqueId)] = [0, 0, 3]
                pointsAlreadyDoneForLines.append((uniqueId, point.getId()))
            pointsDict[point.getId()] = point    
        self.setPointsDict(pointsDict)

    def getPoints(self):
        return self.points
    def setAnts(self, ants):
        self.ants = ants
    def getAnts(self):
        return self.ants
    def setPointsDict(self, pointsDict):
        self.pointsDict = pointsDict
    def getPointsDict(self):
        return self.pointsDict
    def setSuccessfulAnts(self, successfulAnts):
        self.successfulAnts = successfulAnts
    def getSuccessfulAnts(self):
        return self.SuccessfulAnts
    def setLiveAnts(self, liveAnts):
        self.liveAnts = liveAnts
    def getLiveAnts(self):
        return self.liveAnts



    def go(self, display, ant):
        if ant.targetPoint == None:
            indexList = []
            weightsList = []
            trailsValues = ant.currentPoint.getTrailValues()
            pathAsDict = Counter(ant.path)
            weightSum = 0
            for uniqueId, weight in trailsValues.items():
                if uniqueId == ant.lastPoint.uniqueId and len(list(trailsValues.keys())) != 1: continue
                weightSum += weight
            for uniqueId, weight in trailsValues.items():
                
                if uniqueId == ant.lastPoint.uniqueId and len(list(trailsValues.keys())) != 1: continue
                if uniqueId in ant.path: 
                    weightsList.append(weight / (weightSum * (3 * pathAsDict[uniqueId])))
                else: weightsList.append(weight / weightSum) 
                indexList.append(uniqueId)
        
            try:chosenPointIndex = random.choices(indexList, weights=weightsList, k = 1)[0]
            except:
                print(len(indexList), len(weightsList))
                quit()
            for uniqueId, weight in trailsValues.items():
                if uniqueId == chosenPointIndex:
                    ant.targetPoint = self.pointsDict[uniqueId]
                    break
        
        if 0.95 < ant.location[0] / ant.targetPoint.x < 1.05 and 0.95 < ant.location[1] / ant.targetPoint.y< 1.05:
            ant.path.append(ant.targetPoint.getId())

            if ant.targetPoint.getId() == self.endPoint.getId():
                self.liveAnts -= 1
                ant.setActiveStatus(False)
                self.successfulAnts.append(ant)
                return

            ant.location[0] = ant.targetPoint.x
            ant.location[1] = ant.targetPoint.y
            ant.lastPoint = ant.currentPoint
            ant.currentPoint = ant.targetPoint
            ant.targetPoint = None
        else:
            direction = [ant.targetPoint.x - ant.currentPoint.x, ant.targetPoint.y - ant.currentPoint.y]
            direction = [feature / math.sqrt(pow(ant.targetPoint.x - ant.currentPoint.x, 2) + pow(ant.targetPoint.y - ant.currentPoint.y, 2)) for feature in direction]
            ant.location[0] += ant.speed*direction[0]
            ant.location[1] += ant.speed*direction[1]
            # rect = pygame.Rect(0, 0, 15, 15)
            # rect.center = (ant.location[0], ant.location[1])
            # pygame.draw.rect(display,[255, 0, 0],rect)

            pygame.draw.circle(display, [0, 255, 0], [ant.location[0], ant.location[1]], 12)

            # s = pygame.Surface((16,16))  # the size of your rect
            # s.set_alpha(158)                # alpha level
            # s.fill((0, 200, 0))           # this fills the entire surface
            
            # display.blit(s, (ant.location[0] - 8, ant.location[1] - 8))

    def createAnts(self):
        if self.startPoint == None or self.endPoint == None: 
            print("No start/end point")
            return
        for i in range(self.n):
            self.ants.append(Ant(self.startPoint, self.endPoint))
        self.liveAnts = self.n

    def handleKeys(self):
        pause = False
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==K_p:
                    pause = True
                elif event.key  == pygame.K_r:
                    self.setPoints(Points(n=300,r=40, width=self.width, height=self.height))
                    self.epoch = 0
                    self.avgPathByEpoch = []
                    self.successfulAnts = []

                elif event.key  == pygame.K_n:
                    xpoints = [number for number in range(0, self.epoch)]
                    ypoints1 = self.avgPathByEpoch
                    ypoints2 = self.successfulAntsByEpoch

                    fig, ax1 = plt.subplots()
                    fig.set_figheight(6)
                    fig.set_figwidth(6)
                    fig.set_dpi(160)
                    fig.suptitle("Path lenght and number of succ. ants by epoch")

                    ax2 = ax1.twinx()
                    ax1.plot(xpoints, ypoints1, 'r--')
                    ax2.plot(xpoints, ypoints2, 'g-')

                    ax1.set_xlabel("Number of epochs")
                    ax1.set_ylabel('Average path length', color="r")
                    ax2.set_ylabel('Successful ants', color="g")

                    plt.show()
                elif event.key == pygame.K_s:
                    mouseLoc = pygame.mouse.get_pos()
                    for point in self.points.points:
                        collide = point.rect.collidepoint(mouseLoc)
                        if collide: 
                            point.color = [255, 0, 0] if point.color == [0, 0, 0] else [0, 0, 0]
                            point.isStartEnd = True
                            self.startPoint = point
                elif event.key == pygame.K_e:
                    mouseLoc = pygame.mouse.get_pos()
                    for point in self.points.points:
                        collide = point.rect.collidepoint(mouseLoc)
                        if collide: 
                            point.color = [0, 255, 0] if point.color == [0, 0, 0] else [0, 0, 0]
                            point.isStartEnd = True
                            self.endPoint = point
                elif event.key == pygame.K_a:
                    self.createAnts()
        while pause == True:
            for event in pygame.event.get():
                if event.type==KEYUP:
                    if event.key==K_p:
                        pause = False

    def drawStuff(self, display):
        for pointTuple, color in self.linesColor.items():
            pygame.draw.line(display, [color[0], 0, 0], [self.pointsDict[pointTuple[0]].x, self.pointsDict[pointTuple[0]].y], [self.pointsDict[pointTuple[1]].x, self.pointsDict[pointTuple[1]].y], width=color[2])
        for point in self.points.points:
            pygame.draw.rect(display, [255, 255, 255], point.rect)
            pygame.draw.circle(display, point.color, [point.x, point.y], 20 if point.isStartEnd else 12)

        for ant in self.ants:
            if not ant.getActiveStatus(): continue
            if len(ant.path) > self.maxNodesAllowedToVisit: 
                self.liveAnts -= 1
                ant.setActiveStatus(False)
                continue
            self.go(display, ant)
        if self.liveAnts == 0 :
            self.updateTrails()
            for ant in self.ants:
                ant.setActiveStatus(True)
            self.ants = []
            self.createAnts()

    def updateTrails(self):
        pathCosts = []
        self.epoch += 1
        print("Epoch ", self.epoch)
        print("Succesful ants: ", len(self.successfulAnts))
        self.successfulAntsByEpoch.append(len(self.successfulAnts))
        self.liveAnts = self.n
        pathSum = 0
        if len(self.successfulAnts) == 0: 
            print("Average path length: inf")
            print("Best ant's path lenght: inf")
            print("-"*40)
            return
        bestAntPathLength = self.maxNodesAllowedToVisit
        bestPath = None
        for ant in self.successfulAnts:
            if ant.evaluatePath(True, False) < bestAntPathLength: 
                bestPath = ant.path
                bestAntPathLength = ant.evaluatePath(True, False) 
            antSolutionCost =  (self.maxNodesAllowedToVisit)*6 / pow(ant.evaluatePath(True, False), 2)
            pathSum += ant.evaluatePath(True, False)
            pathCost = []
            for index, pointId in enumerate(ant.path):
                if index + 1 == len(ant.path): continue
                pathCost.append((pointId, ant.path[index + 1], antSolutionCost))
            pathCosts.append(pathCost)
        print("Average path length: ", (pathSum + (len(self.ants) - len(self.successfulAnts))*self.maxNodesAllowedToVisit) / len(self.ants))
        if self.maxNodesAllowedToVisit > 3*bestAntPathLength:
            self.maxNodesAllowedToVisit = 3*bestAntPathLength
        print("Best ant's path lenght: ", bestAntPathLength)
        self.avgPathByEpoch.append(pathSum / len(self.successfulAnts))
        print("-"*40)
        self.evaporateTrials()

        for pathCost in pathCosts:
            for data in pathCost:
                point0 = self.pointsDict[data[0]]

                trailValues0 = point0.getTrailValues()

                trailValues0[data[1]] += data[2]
                point0.setTrailValues(trailValues0)

        bestPathCost = []
        for index, pointId in enumerate(bestPath):
            if index + 1 == len(bestPath): continue
            bestPathCost.append((pointId, bestPath[index + 1]))
        for data in bestPathCost:
            try: color = self.linesColor[(data[0], data[1])]
            except: color = self.linesColor[(data[1], data[0])]

            color[0] = 255
            color[2] = 10 # width
            
            try: self.linesColor[(data[0], data[1])] = color
            except: self.linesColor[(data[1], data[0])] = color

        self.successfulAnts = []

        if self.epoch == 20:
            xpoints = [number for number in range(0, self.epoch)]
            ypoints1 = self.avgPathByEpoch
            ypoints2 = self.successfulAntsByEpoch

            fig, ax1 = plt.subplots()
            fig.set_figheight(6)
            fig.set_figwidth(6)
            fig.set_dpi(160)
            fig.suptitle("Path lenght and number of succ. ants by epoch")

            ax2 = ax1.twinx()
            ax1.plot(xpoints, ypoints1, 'r--')
            ax2.plot(xpoints, ypoints2, 'g-')

            ax1.set_xlabel("Number of epochs")
            ax1.set_ylabel('Average path length', color="r")
            ax2.set_ylabel('Successful ants', color="g")

            plt.show()

    def evaporateTrials(self):
        for point in self.points.points:
            newTrailValues = copy.deepcopy(point.trailsValues)
            trailValues = point.trailsValues
            for uniqueId, weight in trailValues.items():
                newTrailValues[uniqueId] = weight*0.9
            point.trailsValues = newTrailValues 
        
        for pointTuple, color in self.linesColor.items():
            if color[0] > 0: ## line is red, turn it black
                color[0] = 0
                color[2] = 3 # width
            self.linesColor[pointTuple] = color

