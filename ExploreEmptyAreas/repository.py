# -*- coding: utf-8 -*-

from domain import *


class Repository:
    def __init__(self):
        self.__populations = []
        self.__averageFitness = []
        self.__standardDeviation = []
        self.drone_map = Map()

    def createPopulation(self, startX, startY, populationSize=50, individualSize=15):
        return Population(populationSize, individualSize, self.drone_map, startX, startY)

    def getMap(self):
        return self.drone_map

    def addPopulation(self, population):
        self.__populations.append(population)

    def randomMap(self):
        self.drone_map.randomMap()

    def loadMap(self, file):
        self.drone_map.loadMap(file)

    def saveMap(self, file):
        self.drone_map.saveMap(file)

    def getLastPopulation(self):
        return self.__populations.pop()

    def peekAtPopulation(self):
        return self.__populations[-1]

    def addAnAverageFitness(self, fitness):
        self.__averageFitness.append(fitness)

    def reset(self):
        self.__averageFitness = []
        self.__standardDeviation = []

    def getAverageFitnessValues(self):
        return self.__averageFitness
