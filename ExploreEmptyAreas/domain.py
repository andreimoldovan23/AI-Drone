# -*- coding: utf-8 -*-
import copy
import pickle
from random import *
from utils import *
import numpy as np


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def saveMap(self, numFile="test.drone_map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)

    def loadMap(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string


class Gene:
    def __init__(self):
        self.__move = choice(variations)

    def getMove(self):
        return self.__move

    def __str__(self):
        return str(self.__move)


class Individual:
    def __init__(self, size=0, drone_map=Map(), start_x=0, start_y=0):
        self.__map = drone_map
        self.__x_drone = start_x
        self.__y_drone = start_y
        self.__size = size
        self.__genome = [Gene()]
        self.__genome.extend(self.__generateGenes() for _ in range(1, self.__size))
        self.__fitness = None

    def __generateGenes(self):
        gene = Gene()
        while gene.getMove()[0] == -1 * self.__genome[-1].getMove()[0] and \
                gene.getMove()[1] == -1 * self.__genome[-1].getMove()[1]:
            gene = Gene()
        return gene

    def __str__(self):
        string = ""
        for gene in self.__genome:
            string += " " + str(gene)
        string += "\nfitness ->" + str(self.fitness()) + " "
        return string

    def getGenome(self):
        return copy.deepcopy(self.__genome)

    def validateCoord(self, x, y):
        if x >= 20 or y >= 20:
            return False
        if x < 0 or y < 0:
            return False

        if self.__map.surface[x][y] == 1:
            return False

        return True

    def __getEmptySquaresFromPos(self, x, y):
        total = 1

        temp_y = y
        temp_x = x + 1
        while temp_x < self.__map.n and self.__map.surface[temp_x][temp_y] == 0:
            total += 1
            temp_x += 1

        temp_x = x - 1
        while temp_x >= 0 and self.__map.surface[temp_x][temp_y] == 0:
            total += 1
            temp_x -= 1

        temp_x = x
        temp_y = y + 1
        while temp_y < self.__map.m and self.__map.surface[temp_x][temp_y] == 0:
            total += 1
            temp_y += 1

        temp_y = y - 1
        while temp_y >= 0 and self.__map.surface[temp_x][temp_y] == 0:
            total += 1
            temp_y -= 1

        return total

    def fitness(self):
        total = self.__getEmptySquaresFromPos(self.__x_drone, self.__y_drone)

        visited = [[self.__x_drone, self.__y_drone]]

        temp_x = self.__x_drone
        temp_y = self.__y_drone
        for gene in self.__genome:
            pos = gene.getMove()
            temp_x += pos[0]
            temp_y += pos[1]

            flag = self.validateCoord(temp_x, temp_y)
            if not flag or [temp_x, temp_y] in visited:
                total -= 10
                break

            # if [temp_x, temp_y] in visited:
            #     total -= 10
            # else:
            #     total += 1 + self.__getEmptySquaresFromPos(temp_x, temp_y)
            #     visited.append([temp_x, temp_y])
            total += 1 + self.__getEmptySquaresFromPos(temp_x, temp_y)
            visited.append([temp_x, temp_y])

        return 0 if total < 0 else total

    def mutate(self, mutateProbability=0.1):
        if random() < mutateProbability:
            pos = randint(0, self.__size - 1)
            gene = Gene()
            while gene.getMove() == self.__genome[pos]:
                gene = Gene()
            self.__genome[pos] = gene

    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.__size, self.__map, self.__x_drone, self.__y_drone), \
                                 Individual(self.__size, self.__map, self.__x_drone, self.__y_drone)
        if random() < crossoverProbability:
            n = self.__size // 3
            parent = True
            for i in range(self.__size):
                if parent:
                    offspring1.__genome[i] = self.__genome[i]
                    offspring2.__genome[i] = otherParent.__genome[i]
                else:
                    offspring1.__genome[i] = otherParent.__genome[i]
                    offspring2.__genome[i] = self.__genome[i]
                if i % n == 0:
                    parent = not parent

        return offspring1, offspring2


class Population:
    def __init__(self, populationSize=50, individualSize=15, drone_map=Map(), drone_x=0, drone_y=0):
        self.__map = drone_map
        self.__drone_x = drone_x
        self.__drone_y = drone_y
        self.__averageFitness = 0.0
        self.__populationSize = populationSize
        self.__individuals = [Individual(individualSize, self.__map, self.__drone_x, self.__drone_y)
                              for _ in range(populationSize)]
        self.__fitness = []

    def evaluate(self):
        total = 0.0
        for x in self.__individuals:
            self.__fitness.append((x, x.fitness()))
            total += x.fitness()
        self.__averageFitness = total / self.__populationSize

    def selection(self, k=0):
        finalList = []
        registered_positions = []
        self.__fitness.sort(key=lambda x: x[1], reverse=True)
        self.__individuals.sort(key=lambda x: x.fitness(), reverse=True)
        for i in range(0, 7 * k // 8):
            finalList.append(self.__fitness[i][0])
        for i in range(7 * k // 8, k):
            pos = randint(7 * k // 8, self.__populationSize - 1)
            while pos in registered_positions:
                pos = randint(7 * k // 8, self.__populationSize - 1)
            finalList.append(self.__individuals[pos])
            registered_positions.append(pos)
        return finalList

    def trim(self):
        self.__fitness.sort(key=lambda x: x[1], reverse=True)
        while len(self.__fitness) > self.__populationSize:
            indv, _ = self.__fitness.pop()
            self.__individuals.remove(indv)

    def getIndividuals(self):
        return self.__individuals

    def getSize(self):
        return self.__populationSize

    def setIndividuals(self, indvs):
        self.__individuals = indvs

    def getAverage(self):
        return self.__averageFitness
