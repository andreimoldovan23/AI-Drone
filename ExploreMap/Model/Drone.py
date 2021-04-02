# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:26:20 2021

@author: moldo
"""

from Model.Map import *


class Drone:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__squareStack = []
        self.__visited = [(self.__x, self.__y)]

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    # moves the drone on an axis in a direction
    def __moveOnAxis(self, pressed_keys, key, directionX, directionY, limit, detectedMap):
        # compare an element with a limit based on direction
        compareWithLimit = lambda a, direction: (a > limit if direction == -1 else a < limit)
        # compare X with a limit if the direction of Y is 0 and vice versa
        checkCondition = ((lambda: compareWithLimit(self.__x, directionX))
                          if directionY == 0
                          else (lambda: compareWithLimit(self.__y, directionY)))
        # move X or Y
        if checkCondition():
            square = detectedMap.getSquare(self.__x + directionX, self.__y + directionY)
            if pressed_keys[key] and square == 0:
                self.__x += directionX
                self.__y += directionY

    # moves the drone
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        # move up
        self.__moveOnAxis(pressed_keys, pygame.K_UP, -1, 0, 0, detectedMap)
        # move down
        self.__moveOnAxis(pressed_keys, pygame.K_DOWN, 1, 0, detectedMap.getNumberRows() - 1, detectedMap)
        # move left
        self.__moveOnAxis(pressed_keys, pygame.K_LEFT, 0, -1, 0, detectedMap)
        # move right
        self.__moveOnAxis(pressed_keys, pygame.K_RIGHT, 0, 1, detectedMap.getNumberColumns() - 1, detectedMap)

    # appends the unvisited neighbour on a given axis in a given direction to the squareStack
    def __selectNeighbours(self, directionX, directionY, limit, detectedMap):
        # compare an element with a limit based on direction
        compareWithLimit = lambda a, direction: (a > limit if direction == -1 else a < limit)
        # compare X with a limit if the direction of Y is 0 and vice versa
        checkCondition = ((lambda: compareWithLimit(self.__x, directionX))
                          if directionY == 0
                          else (lambda: compareWithLimit(self.__y, directionY)))
        x = self.__x + directionX
        y = self.__y + directionY

        # move on X or on Y
        if checkCondition():
            square = detectedMap.getSquare(x, y)
            if square == 0 and (x, y) not in self.__visited:
                # if the square was in unvisited stack and we pass by it again move it forward in the stack
                if (x, y) in self.__squareStack:
                    self.__squareStack.remove((x, y))
                self.__squareStack.append((x, y))

    # appends all unvisited neighbours to the square stack
    def __appendNeighboursUnvisited(self, detectedMap):
        self.__selectNeighbours(-1, 0, 0, detectedMap)
        self.__selectNeighbours(0, -1, 0, detectedMap)
        self.__selectNeighbours(1, 0, detectedMap.getNumberRows() - 1, detectedMap)
        self.__selectNeighbours(0, 1, detectedMap.getNumberColumns() - 1, detectedMap)

    def moveDSF(self, detectedMap):
        # append neighbours
        self.__appendNeighboursUnvisited(detectedMap)
        # terminate program if everything was visited
        if len(self.__squareStack) == 0:
            return

        # get the neighbour positions
        possiblePositions = []
        for el in variation:
            possiblePositions.append((self.__x + el[0], self.__y + el[1]))

        # go to closest unvisited neighbour
        index = len(self.__squareStack) - 1
        while index >= 0 and self.__squareStack[index] not in possiblePositions:
            index -= 1

        # if there are no unvisited neighbours go to previous visited square
        if index == -1:
            # get one of the neighbouring visited squares
            previousSquare = self.__visited.index((self.__x, self.__y)) - 1
            while self.__visited[previousSquare] not in possiblePositions:
                previousSquare -= 1
            self.__x, self.__y = self.__visited[previousSquare]

        # visit neighbour
        else:
            self.__x, self.__y = self.__squareStack.pop(index)
            self.__visited.append((self.__x, self.__y))
