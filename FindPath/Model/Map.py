import numpy as np
import random
import pickle
import pygame

# Creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Map:
    def __init__(self, n=20, m=20):
        self.__n = n
        self.__m = m
        self.__surface = np.zeros((self.__n, self.__m))

    def randomMap(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random.random() <= fill:
                    self.__surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j])) + " "
            string = string + "\n"
        return string

    def getNumberRows(self):
        return self.__n

    def getNumberColumns(self):
        return self.__m

    def getSurface(self):
        return self.__surface

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)

    def loadMap(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.n
            self.__m = dummy.m
            self.__surface = dummy.surface

    def image(self, colour=BLACK, background=WHITE):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        image.fill(background)
        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    image.blit(brick, (j * 20, i * 20))
        return image
