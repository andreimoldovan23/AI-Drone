from Model.Drone import *


class Controller:
    def __init__(self, mapGame, drone):
        self.__map = mapGame
        self.__drone = drone

    @staticmethod
    def __heuristic(start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def __isValid(self, pos):
        return 0 <= pos[0] < self.__map.getNumberRows() and 0 <= pos[1] < self.__map.getNumberColumns()

    def __isFree(self, pos):
        return self.__map.getSurface()[pos[0], pos[1]] == 0

    @staticmethod
    def __reconstructPath(current, start, parents):
        path = []
        while current != start:
            path.append(current)
            current = parents[current]
        path.append(current)
        return path[::-1]

    def __searchAStar(self, initialX, initialY, finalX, finalY):
        toVisit = {}
        visited = []
        gCost = {}
        parents = {}

        start = (initialX, initialY)
        goal = (finalX, finalY)
        toVisit[start] = 0
        gCost[start] = 0

        while len(toVisit) > 0:
            current = next(iter(toVisit))
            toVisit.pop(current)
            visited.append(current)

            if current == goal:
                return Controller.__reconstructPath(current, start, parents)

            neighbours = [(current[0] - 1, current[1]), (current[0], current[1] + 1), (current[0] + 1, current[1]),
                          (current[0], current[1] - 1)]
            for nextNeighbour in neighbours:
                if self.__isValid(nextNeighbour) and self.__isFree(nextNeighbour) and nextNeighbour not in visited:
                    new_cost = gCost[current] + 1
                    if nextNeighbour not in gCost or new_cost < gCost[nextNeighbour]:
                        gCost[nextNeighbour] = new_cost
                        fCost = new_cost + self.__heuristic(nextNeighbour, goal)
                        toVisit[nextNeighbour] = fCost
                        parents[nextNeighbour] = current

            toVisit = {k: v for k, v in sorted(toVisit.items(), key=lambda item: item[1])}

        raise ValueError("Could not find path")

    def __searchGreedy(self, initialX, initialY, finalX, finalY):
        toVisit = {}
        visited = []
        parents = {}

        start = (initialX, initialY)
        goal = (finalX, finalY)
        toVisit[start] = 0

        while len(toVisit) > 0:
            current = next(iter(toVisit))
            toVisit.pop(current)
            visited.append(current)

            if current == goal:
                return Controller.__reconstructPath(current, start, parents)

            neighbours = [(current[0] - 1, current[1]), (current[0], current[1] + 1), (current[0] + 1, current[1]),
                          (current[0], current[1] - 1)]
            for nextNeighbour in neighbours:
                if self.__isValid(nextNeighbour) and self.__isFree(nextNeighbour) and nextNeighbour not in visited:
                    new_cost = self.__heuristic(nextNeighbour, goal)
                    if nextNeighbour not in toVisit or new_cost < toVisit[nextNeighbour]:
                        toVisit[nextNeighbour] = new_cost
                        parents[nextNeighbour] = current

            toVisit = {k: v for k, v in sorted(toVisit.items(), key=lambda item: item[1])}

        raise ValueError("Could not find path")

    def search(self, option, x, y, gX, gY):
        return self.__searchAStar(x, y, gX, gY) if option == 2 else self.__searchGreedy(x, y, gX, gY)

    def setDronePosition(self, x, y):
        self.__drone.setPosition(x, y)

    def autoDrive(self, path):
        pos = path[0]
        positionX = pos[0]
        positionY = pos[1]
        self.__drone.setPosition(positionX, positionY)
        return path.pop(0), path

    def getMapImage(self):
        return self.__map.image()

    def getMapWithDroneImage(self, img):
        return self.__drone.mapWithDrone(img)

    def generateMap(self, option):
        self.__map.loadMap("Resources/test1.map") if option == 1 else self.__map.randomMap()
