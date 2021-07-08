from numpy import append, unicode_
import pygame
import sys

from pygame.constants import K_RETURN
from pygame.font import Font


# pressedKeys = []
class command:
    def __init__(self, cColor, cRect) -> None:
        self.rect = cRect
        self.color = cColor

    def getRect(self):
        return self.rect


class keyPress:
    def __init__(self, cmnd: command, mFont: Font) -> None:
        self.pressedKeys = []
        self.command = cmnd
        self.rect = self.command.rect
        self.font = mFont

    def processInstruct(self, instructString: list):

        # instructionString format ABXY

        # AB denotes type of transformation
        # XY specify numerical values associated with transformation

        # for x in instructString:
        #     print(pygame.key.name(x))

        # Checking for transformation type
        # Length less than 2 causes index range error
        if (len(instructString) > 2 and pygame.key.name(instructString[0]) +
                pygame.key.name(instructString[1]) == 'rn'):
            print("rotate")
            # call roation function with parameters pygame.key.name(instructString[2]) and more

    def keyPressed(self, eventKey):

        self.pressedKeys.append(eventKey)
        # print(self.pressedKeys)
        if eventKey == pygame.K_q:
            sys.exit()

        elif eventKey == pygame.K_RETURN:
            self.processInstruct(self.pressedKeys)
            self.pressedKeys.clear()

    def getRectCor(self):
        self.rect = self.command.getRect()

    def getPressedKeysStr(self):
        kStr = ''
        for x in self.pressedKeys:
            kStr = kStr + pygame.key.name(x)
        return kStr
        return self.pressedKeys


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
