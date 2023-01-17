

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
        self.maxNodesAllowedToVisit = 25
        self.liveAnts = None
        self.startPoint = None
        self.endPoint = None
        self.points = None
        self.ants = []
        self.successfulAnts = []
        self.pointsDict = None
        self.linesColor = {}
        self.avgPaths = []
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
        for point in self.points.points:
            trailValues = point.getTrailValues()
            for uniqueId, value in trailValues.items():
                self.linesColor[(point.getId(), uniqueId)] = [0, 0]

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
                weightSum += weight
            for uniqueId, weight in trailsValues.items():
                if uniqueId in ant.path: 
                    weightsList.append(weight / (weightSum * (3 + pathAsDict[uniqueId])))
                else: weightsList.append(weight / weightSum) 
                indexList.append(uniqueId)
            if not sum(weightsList) > 0:
                for i in range(0, len(weightsList)):
                    weightsList[i] = 1 
            chosenPointIndex = random.choices(indexList, weights=weightsList, k = 1)[0]
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
            ant.currentPoint = ant.targetPoint
            ant.targetPoint = None
        else:
            direction = [ant.targetPoint.x - ant.currentPoint.x, ant.targetPoint.y - ant.currentPoint.y]
            direction = [feature / math.sqrt(pow(ant.targetPoint.x - ant.currentPoint.x, 2) + pow(ant.targetPoint.y - ant.currentPoint.y, 2)) for feature in direction]
            ant.location[0] += ant.speed*direction[0]
            ant.location[1] += ant.speed*direction[1]
            rect = pygame.Rect(0, 0, 10, 10)
            rect.center = (ant.location[0], ant.location[1])
            pygame.draw.rect(display,[255, 0, 0],rect)

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
                    self.setPoints(Points(n=140,r=45, width=self.width, height=self.height))
                elif event.key  == pygame.K_n:
                    xpoints = [number for number in range(0, self.epoch)]
                    ypoints = self.avgPaths

                    plt.plot(xpoints, ypoints)
                    plt.title("Path lenght by epoch")
                    plt.xlabel("Number of epochs")
                    plt.ylabel("Average path length")
                    plt.show()
                elif event.key == pygame.K_s:
                    mouseLoc = pygame.mouse.get_pos()
                    for point in self.points.points:
                        collide = point.rect.collidepoint(mouseLoc)
                        if collide: 
                            point.color = [255, 0, 0] if point.color == [255, 255, 255] else [255, 255, 255]
                            point.isStartEnd = True
                            self.startPoint = point
                elif event.key == pygame.K_e:
                    mouseLoc = pygame.mouse.get_pos()
                    for point in self.points.points:
                        collide = point.rect.collidepoint(mouseLoc)
                        if collide: 
                            point.color = [0, 255, 0] if point.color == [255, 255, 255] else [255, 255, 255]
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
            if color[0] > 255: color[0] = 255
            if color[1] > 255: color[1] = 255
            pygame.draw.line(display, [255, 255 - color[0], 255 - color[1]], [self.pointsDict[pointTuple[0]].x, self.pointsDict[pointTuple[0]].y], [self.pointsDict[pointTuple[1]].x, self.pointsDict[pointTuple[1]].y], width=2)
        for point in self.points.points:
            pygame.draw.rect(display, [0, 0, 0], point.rect)
            pygame.draw.circle(display, point.color, [point.x, point.y], 18 if point.isStartEnd else 9)

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
        print("Im updating the trails")
        print("Succesful ants: ", len(self.successfulAnts))
        self.liveAnts = self.n
        pathSum = 0
        if len(self.successfulAnts) == 0: return
        for ant in self.successfulAnts:
            antSolutionCost =  (self.maxNodesAllowedToVisit) * 2.5 / (ant.evaluatePath(True, False) * 50)
            pathSum += ant.evaluatePath(True, False)
            pathCost = []
            for index, pointId in enumerate(ant.path):
                if index + 1 == len(ant.path): continue
                pathCost.append((pointId, ant.path[index + 1], antSolutionCost))
            pathCosts.append(pathCost)
        print("Average path length: ", pathSum / len(self.successfulAnts))
        self.avgPaths.append(pathSum / len(self.successfulAnts))
        print("-"*40)
        for pathCost in pathCosts:
            for data in pathCost:
                point0 = self.pointsDict[data[0]]

                trailValues0 = point0.getTrailValues()

                trailValues0[data[1]] += data[2]
                point0.setTrailValues(trailValues0)

                if self.linesColor[(data[0], data[1])][1] > 255:
                    self.linesColor[(data[0], data[1])][0] += data[2]
                self.linesColor[(data[0], data[1])][1] += data[2]


        self.evaporateTrials()
        self.successfulAnts = []

    def evaporateTrials(self):
        for point in self.points.points:
            newTrailValues = copy.deepcopy(point.getTrailValues())
            trailValues = point.getTrailValues()
            for uniqueId, weight in trailValues.items():
                newTrailValues[uniqueId] -= 1
            point.setTrailValues(newTrailValues)

