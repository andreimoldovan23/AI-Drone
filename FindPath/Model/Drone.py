from Model.Map import *


class Drone:
    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.__x > 0:
            if pressed_keys[pygame.K_UP] and detectedMap.getSurface()[self.__x - 1][self.__y] == 0:
                self.__x = self.__x - 1
        if self.__x < 19:
            if pressed_keys[pygame.K_DOWN] and detectedMap.getSurface()[self.__x + 1][self.__y] == 0:
                self.__x = self.__x + 1

        if self.__y > 0:
            if pressed_keys[pygame.K_LEFT] and detectedMap.getSurface()[self.__x][self.__y - 1] == 0:
                self.__y = self.__y - 1
        if self.__y < 19:
            if pressed_keys[pygame.K_RIGHT] and detectedMap.getSurface()[self.__x][self.__y + 1] == 0:
                self.__y = self.__y + 1

    def setPosition(self, x, y):
        self.__x = x
        self.__y = y

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("Resources/drona.png")
        mapImage.blit(drona, (self.__y * 20, self.__x * 20))
        return mapImage
