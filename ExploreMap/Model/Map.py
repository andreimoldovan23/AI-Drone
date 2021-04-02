# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:26:18 2021

@author: moldo
"""
from Model.Enviroment import *


class DMap:
    def __init__(self, x, y):
        self.__n = x
        self.__m = y
        self.__surface = np.full((self.__n, self.__m), -1)

    def __markOnAxis(self, freeSquares, x, y, directionX, directionY, limit):
        tempX = x + directionX
        tempY = y + directionY

        # compares an element with a limit based on direction
        compareWithLimit = lambda a, direction: (a >= limit if direction == -1 else a < limit)

        # compares a position with the number of empty positions based on direction
        compareWithFreeSquares = lambda a, b, direction: (
            a >= b - freeSquares if direction == -1 else a <= b + freeSquares)

        # condition for loop, checks for X or Y
        loopCondition = ((lambda a, b: compareWithLimit(a, directionX) and compareWithFreeSquares(a, x, directionX))
                         if directionY == 0
                         else (
            lambda a, b: compareWithLimit(b, directionY) and compareWithFreeSquares(b, y, directionY)))

        # a condition to check if a square is a brick or not
        fillSquareCondition = ((lambda a, b: compareWithLimit(a, directionX))
                               if directionY == 0
                               else (lambda a, b: compareWithLimit(b, directionY)))

        # mark empty squares
        if freeSquares > 0:
            while loopCondition(tempX, tempY):
                self.__surface[tempX][tempY] = 0
                tempX += directionX
                tempY += directionY
        # mark brick
        if fillSquareCondition(tempX, tempY):
            self.__surface[tempX][tempY] = 1

    # mark detected bricks in all directions
    def markDetectedWalls(self, env, x, y):
        walls = env.readUDMSensors(x, y)
        self.__markOnAxis(walls[UP], x, y, variation[0][0], variation[0][1], 0)
        self.__markOnAxis(walls[DOWN], x, y, variation[1][0], variation[1][1], self.__n)
        self.__markOnAxis(walls[LEFT], x, y, variation[2][0], variation[2][1], self.__m)
        self.__markOnAxis(walls[RIGHT], x, y, variation[3][0], variation[3][1], 0)
        return None

    def getSquare(self, x, y):
        return self.__surface[x][y]

    def getNumberRows(self):
        return self.__n

    def getNumberColumns(self):
        return self.__m

    def image(self, x, y, color=BLACK, emptyColor=WHITE, background=GRAYBLUE):
        playMapSurface = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        emptyBrick = pygame.Surface((20, 20))

        emptyBrick.fill(emptyColor)
        brick.fill(color)
        playMapSurface.fill(background)

        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    playMapSurface.blit(brick, (j * 20, i * 20))
                elif self.__surface[i][j] == 0:
                    playMapSurface.blit(emptyBrick, (j * 20, i * 20))

        drona = pygame.image.load("resources/drona.png")
        playMapSurface.blit(drona, (y * 20, x * 20))
        return playMapSurface
