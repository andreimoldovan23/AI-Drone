# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:25:43 2021

@author: moldo
"""

# imports
import pickle
from random import uniform
import numpy as np
import pygame

# define colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

# define indexes variations
variation = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Environment:
    def __init__(self, x, y):
        self.__n = x
        self.__m = y
        self.__surface = np.zeros((self.__n, self.__m))

    def randomMap(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if uniform(0.0, 1.0) <= fill:
                    self.__surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string

    def __readOnAxis(self, xCoord, yCoord, directionX, directionY, limit):
        numberReadings = 0
        tempXCoord = xCoord + directionX
        tempYCoord = yCoord + directionY

        # compare an element with a limit based on direction
        condition = lambda a, direction: (a < limit if direction == 1 else a >= limit)

        # compare X or Y with the limits of the map
        conditionOnCoord = ((lambda a, b: condition(a, directionX))
                            if directionY == 0
                            else (lambda a, b: condition(b, directionY)))

        # count empty squares on X or Y
        while conditionOnCoord(tempXCoord, tempYCoord) and self.__surface[tempXCoord][tempYCoord] == 0:
            tempXCoord += directionX
            tempYCoord += directionY
            numberReadings += 1

        return numberReadings

    # returns number of empty squares in all directions on X and Y
    def readUDMSensors(self, x, y):
        return [
                self.__readOnAxis(x, y, variation[0][0], variation[0][1], 0),
                self.__readOnAxis(x, y, variation[2][0], variation[2][1], self.__m),
                self.__readOnAxis(x, y, variation[1][0], variation[1][1], self.__n),
                self.__readOnAxis(x, y, variation[3][0], variation[3][1], 0)
                ]

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as file:
            pickle.dump(self, file)

    def loadEnvironment(self, numFile):
        with open(numFile, "rb") as file:
            dummy = pickle.load(file)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface

    def image(self, colour=GREEN, background=RED):
        mapSurface = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        mapSurface.fill(background)
        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    mapSurface.blit(brick, (j * 20, i * 20))

        return mapSurface
