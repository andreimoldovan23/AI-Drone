from Controller.Controller import *
import time
import sys


class UI:
    def __init__(self, controller):
        pygame.init()
        logo = pygame.image.load("Resources/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")
        self.__gameScreen = pygame.display.set_mode((400, 400))
        self.__gameScreen.fill(WHITE)
        self.__controller = controller
        self.__initialX = 0
        self.__initialY = 0
        self.__finalX = 0
        self.__finalY = 0

    def __loadScreen(self):
        pressEnter = pygame.image.load("Resources/pressEnter.png")
        enterSurface = pygame.Surface((400, 400))
        enterSurface.fill(GRAYBLUE)
        enterSurface.blit(pressEnter, (0, 0))
        self.__gameScreen.blit(enterSurface, (0, 0))
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
        pressEsc = pygame.image.load("Resources/quit.png")
        quitSurface = pygame.Surface((400, 400))
        quitSurface.fill(WHITE)
        quitSurface.blit(pressEsc, (0, 0))
        self.__gameScreen.blit(quitSurface, (0, 0))
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit(0)

    def __buttonScreen(self, listButtonsText, title):
        smallFont = pygame.font.SysFont('Corbel', 15)
        bigFont = pygame.font.SysFont('Corbel', 35)
        width = 150
        height = 50
        coords = [(33, 100), (216, 100), (33, 250), (216, 250)]
        textTitle = bigFont.render(title, True, BLACK)

        listText = []
        listButtons = []
        for i in range(0, len(listButtonsText)):
            coord = coords[i]
            msg = listButtonsText[i]
            text = smallFont.render(msg, True, BLACK)
            button = pygame.Rect(coord[0], coord[1], width, height)
            listText.append(text)
            listButtons.append(button)

        self.__gameScreen.fill(GRAYBLUE)
        self.__gameScreen.blit(textTitle, (120, 50))

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.__quitScreen()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in listButtons:
                        if button.collidepoint(mouse):
                            return listButtons.index(button) + 1

            for button in listButtons:
                pygame.draw.rect(self.__gameScreen, RED, button)
            for text in listText:
                coord = coords[listText.index(text)]
                self.__gameScreen.blit(text, (coord[0], coord[1]))

            for button in listButtons:
                if button.collidepoint(mouse):
                    text = listText[listButtons.index(button)]
                    coord = coords[listButtons.index(button)]
                    pygame.draw.rect(self.__gameScreen, GREEN, button)
                    self.__gameScreen.blit(text, (coord[0], coord[1]))

            pygame.display.flip()

    @staticmethod
    def __displayWithPath(image, path, destMove):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        destination = pygame.Surface((20, 20))
        destination.fill(RED)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))
        image.blit(destination, (destMove[1] * 20, destMove[0] * 20))
        return image

    def __setCoords(self, x, y, fX, fY, searchOption):
        self.__initialX = x
        self.__initialY = y
        self.__finalX = fX
        self.__finalY = fY
        self.__controller.setDronePosition(self.__initialX, self.__initialY)
        start_time = time.time()
        path = self.__controller.search(searchOption, self.__initialX, self.__initialY, self.__finalX, self.__finalY)
        return start_time, path

    def run(self):
        mapOption = self.__buttonScreen(["I'm playing safe", "Give me a challenge"], "Choose map")
        searchOption = self.__buttonScreen(["Greedy", "A*"], "Search")

        self.__controller.generateMap(mapOption)

        pathFunction = {3: lambda: self.__setCoords(18, 16, 16, 3, searchOption),
                        4: lambda: self.__setCoords(2, 1, 2, 3, searchOption),
                        1: lambda: self.__setCoords(0, 19, 19, 0, searchOption),
                        2: lambda: self.__setCoords(1, 9, 3, 12, searchOption)}
        pathNumber = self.__buttonScreen(["(0, 19) -> (19, 0)", "(1, 9) -> (3, 12)", "(18, 16) -> (16, 3)",
                                          "(2, 1) -> (2, 3)"], "PathNumber")
        start_time, path = pathFunction[pathNumber]()
        self.__loadScreen()

        destMove = path[len(path) - 1]
        walkedThrough = []
        while len(path) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__quitScreen()

            newSpot, path = self.__controller.autoDrive(path)
            walkedThrough.append(newSpot)
            proxyImage = UI.__displayWithPath(self.__controller.getMapImage(), walkedThrough, destMove)
            proxyImage = self.__controller.getMapWithDroneImage(proxyImage)
            self.__gameScreen.blit(proxyImage, (0, 0))
            pygame.display.flip()
            time.sleep(0.3)

        end_Time = time.time()
        print(str(end_Time - start_time) + "s elapsed")

        time.sleep(5)
        self.__quitScreen()
