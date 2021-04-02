import pygame
import sys
from Service.service import *


class Game:
    def __init__(self):
        pygame.init()
        logo = pygame.image.load("resources/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")
        self.__gameScreen = pygame.display.set_mode((800, 400))
        self.__gameScreen.fill(WHITE)
        self.__service = Service()

    def __loadScreen(self):
        pressEnter = pygame.image.load("resources/pressEnter.png")
        enterSurface = pygame.Surface((420, 420))
        enterSurface.fill(GRAYBLUE)
        enterSurface.blit(pressEnter, (0, 0))
        self.__gameScreen.blit(enterSurface, (400, 0))
        pygame.display.flip()

        loading = True
        while loading:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_RETURN]:
                        loading = False
                    elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        self.__quitScreen()

    def __quitScreen(self):
        pressEsc = pygame.image.load("resources/quit.png")
        quitSurface = pygame.Surface((800, 400))
        quitSurface.fill(WHITE)
        quitSurface.blit(pressEsc, (0, 0))
        self.__gameScreen.blit(quitSurface, (0, 0))
        pygame.display.flip()
        sleep(3)
        pygame.quit()
        sys.exit(0)

    def __buttonScreen(self, msg1, msg2, title):
        smallFont = pygame.font.SysFont('Corbel', 35)
        bigFont = pygame.font.SysFont('Corbel', 50)
        text1 = smallFont.render(msg1, True, BLACK)
        text2 = smallFont.render(msg2, True, BLACK)
        textTitle = bigFont.render(title, True, BLACK)
        button1 = pygame.Rect(50, 250, 300, 50)
        button2 = pygame.Rect(450, 250, 300, 50)
        self.__gameScreen.fill(GRAYBLUE)
        self.__gameScreen.blit(textTitle, (250, 50))

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.__quitScreen()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1.collidepoint(mouse):
                        return "yes"
                    elif button2.collidepoint(mouse):
                        return "no"

            pygame.draw.rect(self.__gameScreen, RED, button1)  # draw button
            pygame.draw.rect(self.__gameScreen, RED, button2)
            self.__gameScreen.blit(text1, (60, 250))
            self.__gameScreen.blit(text2, (460, 250))

            if button1.collidepoint(mouse):
                pygame.draw.rect(self.__gameScreen, GREEN, button1)
                self.__gameScreen.blit(text1, (60, 250))
            if button2.collidepoint(mouse):
                pygame.draw.rect(self.__gameScreen, GREEN, button2)
                self.__gameScreen.blit(text2, (460, 250))

            pygame.display.flip()

    def run(self):
        mapOption = self.__buttonScreen("I'm playing safe", "Give me a challenge", "Choose map")
        driveOption = self.__buttonScreen("I want to fly", "Let it have fun", "Who's driving?")
        speedOption = ""
        if driveOption == "no":
            speedOption = self.__buttonScreen("Take me to a cruise", "No time to waste", "Speed")
        self.__service.generateMap(mapOption)

        self.__gameScreen.blit(self.__service.getEnv().image(), (0, 0))
        self.__loadScreen()

        while True:
            self.__service.markWalls()
            self.__gameScreen.blit(self.__service.getMapImage(), (400, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.__quitScreen()
                if driveOption == "yes" and event.type == pygame.KEYDOWN:
                    self.__service.drive()
            if driveOption == "no":
                self.__service.autoDrive(0.1 if speedOption == "no" else 0.5)
