from Model.Drone import *
from random import randint
from time import sleep


class Service:
    def __init__(self):
        self.__env = Environment(20, 20)
        self.__map = DMap(20, 20)
        x = randint(0, self.__map.getNumberRows() - 1)
        y = randint(0, self.__map.getNumberColumns() - 1)
        self.__drone = Drone(x, y)

    def getEnv(self):
        return self.__env

    def getMap(self):
        return self.__map

    def getDrone(self):
        return self.__drone

    def markWalls(self):
        self.__map.markDetectedWalls(
            self.__env, self.__drone.getX(), self.__drone.getY())

    def getMapImage(self):
        return self.__map.image(self.__drone.getX(), self.__drone.getY())

    def drive(self):
        self.__drone.move(self.__map)

    def autoDrive(self, speed):
        sleep(speed)
        self.__drone.moveDSF(self.__map)

    def generateMap(self, mapOption):
        self.__env.randomMap() if mapOption == "no" else self.__env.loadEnvironment("resources/test2.map")
