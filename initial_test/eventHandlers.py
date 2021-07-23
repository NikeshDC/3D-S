import pygame

from pygame.constants import K_RETURN, K_BACKSPACE
from pygame.font import Font
from TransfClasses import *

transformationVals = TransfVars()


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
        # Checking for transformation type
        # Length less than 2 causes index range error

        # --------------------------------------------ROTATION--------------------------------------------
        # ROTATION COMMAND FORMAT => R[DIRECTION][2 DIGIT DEGREE][O FOR ORIGIN][2 DIGIT X VAL][","][2 DIGIT Y VAL]
        # DEFINING ORIGIN IS OPTIONAL
        # PREVIOUSLY SET ORIGIN WILL BE DEFAULT ORIGIN
        if (len(instructString) >= 4
                and pygame.key.name(instructString[0]) == 'r'):
            rotationAngle = int(pygame.key.name(instructString[2])) * 10 + int(
                pygame.key.name(instructString[3]))
            transformationVals.rotateC.setAngle(rotationAngle)
            if (pygame.key.name(instructString[1]) == 'c'):
                transformationVals.rotateC.setDirection(True)
                print("rotate clockwise by ", rotationAngle, " degree")
            elif (pygame.key.name(instructString[1]) == 'a'):
                transformationVals.rotateC.setDirection(False)
                print("Rotate anticlockwise by", rotationAngle, " degree")
            if (len(instructString) == 12
                    and pygame.key.name(instructString[4]) == 'o'
                    and checkKeys.isDigit(instructString[5])
                    and checkKeys.isDigit(instructString[6])
                    and checkKeys.isDigit(instructString[8])
                    and checkKeys.isDigit(instructString[9])
                    and checkKeys.isDigit(instructString[11])
                    and checkKeys.isDigit(instructString[12])):
                rx = int(pygame.key.name(instructString[5])) * 10 + int(
                    pygame.key.name(instructString[6]))
                ry = int(pygame.key.name(instructString[8])) * 10 + int(
                    pygame.key.name(instructString[9]))
                rz = int(pygame.key.name(instructString[11])) * 10 + int(
                    pygame.key.name(instructString[12]))
                transformationVals.rotateC.setFixedPoint(Coord(rx, ry, rz))
                print("Origin changed to: (", rx, ",", ry, ",", rz, ")")

        # --------------------------------------------TRANSLATION--------------------------------------------
        # TRANSLATION COMMAND FORMAT => T[]
        elif (len(instructString) == 4
              and pygame.key.name(instructString[0]) == 't'):
            print("translate")
        # --------------------------------------------SCALLING--------------------------------------------
        # SCALLING COMMAND FORMAT => T[]
        elif (len(instructString) == 4
              and pygame.key.name(instructString[0]) == 's'):
            print("scale")
        # --------------------------------------------SOMETHING--------------------------------------------
        # SOMETHING COMMAND FORMAT => T[]
        elif (len(instructString) == 4
              and pygame.key.name(instructString[0]) == 'e'):
            print("excrude")

    def processKey(self, eventKey):
        # print(eventKey, " = ", pygame.key.name(eventKey))

        # All Command instructions are aplhanumeric
        # 0 = 48 9 = 57 a= 97 z =122
        if (checkKeys.isAlpha(eventKey) or checkKeys.isDigit(eventKey)
                or eventKey == 44):

            self.pressedKeys.append(eventKey)

        # Backspace key action
        if eventKey == pygame.K_BACKSPACE and len(self.pressedKeys) != 0:
            self.pressedKeys.pop()

        # Enter Key action
        elif eventKey == pygame.K_RETURN:
            # print(self.pressedKeys)
            self.processInstruct(self.pressedKeys)
            self.pressedKeys.clear()
            print(transformationVals.rotateC.getDirection())

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
