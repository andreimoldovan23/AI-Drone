from repository import *
from datetime import datetime
import random


class Controller:
    def __init__(self):
        self.__repo = Repository()
        self.__fitnessChart = []
        self.__startX = 0
        self.__startY = 0
        self.__populationSize = 50
        self.__mutationProbability = 0.1
        self.__crossoverProbability = 0.8
        self.__noOfGenes = 15
        self.__noOfIterations = 100

    def selectStart(self):
        self.__startX = randint(0, 19)
        self.__startY = randint(0, 19)
        while self.__repo.getMap().surface[self.__startX][self.__startY] == 1:
            self.__startX = randint(0, 19)
            self.__startY = randint(0, 19)

    def setup(self, populationSize=50, mutationProbability=0.1, crossoverProbability=0.8, noOfGenes=15,
              noOfIterations=100):
        self.__populationSize = populationSize
        self.__mutationProbability = mutationProbability
        self.__crossoverProbability = crossoverProbability
        self.__noOfGenes = noOfGenes
        self.__noOfIterations = noOfIterations

    def iteration(self, population):
        if population.getAverage() == 0.0:
            population.evaluate()
        fit = copy.deepcopy(population.getAverage())
        self.__repo.addAnAverageFitness(fit)
        survivors = population.selection(self.__populationSize // 2)
        offsprings = []
        i = 1
        while len(survivors) + len(offsprings) < self.__populationSize and i < len(survivors):
            o1, o2 = survivors[i].crossover(survivors[i - 1], self.__crossoverProbability)
            o1.mutate(self.__mutationProbability)
            o2.mutate(self.__mutationProbability)
            offsprings.append(o1)
            offsprings.append(o2)
            i += 1

        survivors.extend(offsprings)
        resultPop = Population(self.__populationSize)
        resultPop.setIndividuals(survivors)
        resultPop.evaluate()
        resultPop.trim()
        return resultPop

    def run(self):
        crt = 0
        self.__fitnessChart = []
        self.__repo.reset()
        while self.__noOfIterations > crt:
            pop = self.__repo.getLastPopulation()
            resultPop = self.iteration(pop)
            self.__repo.addPopulation(resultPop)
            crt += 1

        self.__fitnessChart = [[i for i in range(self.__noOfIterations)], self.__repo.getAverageFitnessValues()]

    def solver(self):
        random.seed(datetime.now().time().second)
        self.selectStart()

        p = self.__repo.createPopulation(self.__startX, self.__startY, self.__populationSize, self.__noOfGenes)
        self.__repo.addPopulation(p)

        self.run()

        return self.__repo.getAverageFitnessValues()

    def randomMap(self):
        self.__repo.randomMap()

    def loadMap(self, file):
        self.__repo.loadMap(file)

    def saveMap(self, file):
        self.__repo.saveMap(file)

    def getMap(self):
        return self.__repo.getMap()

    def getSolution(self):
        indvs = self.__repo.peekAtPopulation().getIndividuals()
        indvs.sort(key=lambda x: x.fitness(), reverse=True)
        sol = indvs[0]
        x = self.__startX
        y = self.__startY
        path = [[x, y]]
        for oneGene in sol.getGenome():
            move = oneGene.getMove()
            if not sol.validateCoord(x + move[0], y + move[1]):
                path.append(path[-1])
            else:
                path.append([x + move[0], y + move[1]])
        return path

    def getFitnessChart(self):
        return self.__fitnessChart
