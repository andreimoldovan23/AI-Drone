# -*- coding: utf-8 -*-


# imports
from time import sleep

from gui import *
from controller import *
from repository import *
from domain import *
from matplotlib import pyplot as plt


class UI:
    def __init__(self):
        self.__controller = Controller()

    def menu(self):
        menuText = "Map options:\na. create random drone_map\nb. load a drone_map" \
                   "\nc. save a drone_map\nd. visualise drone_map"
        menuText += "\nEA options:\ne. parameters setup\nf. run the solver" \
                    "\ng. visualise the statistics\nh. view the drone moving on a path"
        menuText += "\nPlease choose a letter. Press X to exit\n"

        while True:
            input_choice = input(menuText)
            if input_choice == "X":
                break

            if input_choice == "a":
                self.randomMap()

            if input_choice == "b":
                file = input("Tell me the file name: ")
                self.loadMap(file)

            if input_choice == "c":
                file = input("Tell me the file name: ")
                self.saveMap(file)

            if input_choice == "d":
                displayMap(self.seeMap())

            if input_choice == "e":
                try:
                    populationSize = int(input("Tell me the population size: "))
                    mutationProbability = float(input("Tell me the mutation probability: "))
                    crossoverProbability = float(input("Tell me the crossover probability: "))
                    noOfGenes = int(input("Tell me the number of genes for an individual: "))
                    noOfIterations = int(input("Tell me the number of iterations: "))
                    self.parameterSetup(populationSize, mutationProbability, crossoverProbability,
                                        noOfGenes, noOfIterations)
                except ValueError:
                    print("Wrong input")

            if input_choice == "f":
                self.runSolver()

            if input_choice == "g":
                self.statistics()

            if input_choice == "h":
                self.viewSolution()

            if input_choice not in "Xabcdefgh":
                print("Wrong command!")

    def randomMap(self):
        self.__controller.randomMap()

    def loadMap(self, file):
        self.__controller.loadMap(file)

    def saveMap(self, file):
        self.__controller.saveMap(file)

    def seeMap(self):
        return self.__controller.getMap()

    def parameterSetup(self, populationSize=50, mutationProbability=0.1, crossoverProbability=0.8,
                       noOfGenes=15, noOfIterations=100):
        self.__controller.setup(populationSize, mutationProbability, crossoverProbability, noOfGenes, noOfIterations)

    def runSolver(self):
        self.__controller.solver()

    def statistics(self):
        print("Statistics")
        chart = self.__controller.getFitnessChart()
        plt.plot(chart[0], chart[1])
        plt.show()

    def viewSolution(self):
        path = self.__controller.getSolution()
        movingDrone(self.__controller.getMap(), path)
