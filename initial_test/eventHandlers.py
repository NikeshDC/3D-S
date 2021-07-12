import pygame

from pygame.constants import K_RETURN, K_BACKSPACE
from pygame.font import Font


# pressedKeys = []
class CommandWindow:
    def __init__(self, cColor, cRect) -> None:
        self.rect = cRect
        self.color = cColor

    def getRect(self):
        return self.rect


class Command:
    def __init__(self, cmnd: CommandWindow, mFont: Font) -> None:
        self.pressedKeys = []
        self.commandWindow = cmnd
        self.rect = self.commandWindow.rect
        self.font = mFont

    def processInstruct(self, instructString: list):

        # instructionString format ABXY

        # AB denotes type of transformation
        # XY specify numerical values associated with transformation

        # for x in instructString:
        #     print(pygame.key.name(x))

        # Checking for transformation type
        # Length less than 2 causes index range error
        if (len(instructString) == 4
                and pygame.key.name(instructString[0]) == 'r'):
            if (pygame.key.name(instructString[1]) == 'c'):
                print("rotate clockwise")
            elif (pygame.key.name(instructString[1]) == 'a'):
                print("Rotate anticlockwisr")
            # call roation function with parameters pygame.key.name(instructString[2]) and more
        elif (len(instructString) == 4
              and pygame.key.name(instructString[0]) == 't'):
            print("translate")
        elif (len(instructString) == 4
              and pygame.key.name(instructString[0]) == 's'):
            print("scale")
        elif (len(instructString) == 4
              and pygame.key.name(instructString[0]) == 'e'):
            print("excrude")

    def processKey(self, eventKey):
        print(eventKey)
        self.pressedKeys.append(eventKey)
        # print(self.pressedKeys)
        if eventKey == pygame.K_BACKSPACE:
            self.pressedKeys.pop()
        elif eventKey == pygame.K_RETURN:
            self.pressedKeys.pop()
            self.processInstruct(self.pressedKeys)
            self.pressedKeys.clear()

    def getRectCor(self):
        self.rect = self.commandWindow.getRect()

    def getPressedKeysStr(self):
        kStr = ''
        for x in self.pressedKeys:
            kStr = kStr + pygame.key.name(x)
        return kStr


# def processInstruct(instructString: list):

#     # instructionString format ABXY

#     # AB denotes type of transformation
#     # XY specify numerical values associated with transformation

#     # for x in instructString:
#     #     print(pygame.key.name(x))

#     # Checking for transformation type
#     # Length less than 2 causes index range error
#     if (len(instructString) > 2 and pygame.key.name(instructString[0]) +
#             pygame.key.name(instructString[1]) == 'rn'):
#         print("rotate")
#         # call roation function with parameters pygame.key.name(instructString[2]) and more

# def keyPressed(eventKey):

#     pressedKeys.append(eventKey)
#     # print(pressedKeys)
#     if eventKey == pygame.K_q:
#         sys.exit()

#     elif eventKey == pygame.K_RETURN:
#         processInstruct(pressedKeys)
#         pressedKeys.clear()
