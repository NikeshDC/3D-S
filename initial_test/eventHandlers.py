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


print


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
        # ROTATION COMMAND FORMAT => R[AXIS][DEGREE]
        # Minimum command is r[dir](deg) deg is optional
        if (len(instructString) >= 2
                and pygame.key.name(instructString[0]) == 'r'):

            if (checkKeys.isAxesAlpha(pygame.key.name(instructString[1]))):
                transformationVals.rotateC.setDirection(
                    pygame.key.name(instructString[1]))
            else:
                print("Invalid direction\nSelected Default Direction[x]")

            if (len(instructString) > 2):
                rotationAngle = float(strManip.makeStr(instructString[2:]))
                transformationVals.rotateC.setAngle(rotationAngle)
            else:
                transformationVals.rotateC.setAngle()

            print("Rotation about ", transformationVals.rotateC.getDirection(),
                  " by ", transformationVals.rotateC.getAngle(), "degree")

        # --------------------------------------------TRANSLATION--------------------------------------------
        # TRANSLATION COMMAND FORMAT => T[AXIS][VAL[DIST?]]
        elif (len(instructString) >= 2
              and pygame.key.name(instructString[0]) == 't'):

            if (checkKeys.isAxesAlpha(pygame.key.name(instructString[1]))):
                transformationVals.translateC.setDirection(
                    pygame.key.name(instructString[1]))
            else:
                print("Invalid axis\nSelected Default axis[x]")
            if (len(instructString) > 2):
                translationVal = float(strManip.makeStr(instructString[2:]))
                transformationVals.translateC.setTranslVal(translationVal)
            else:
                transformationVals.translateC.setTranslVal()

            print("Translation in ",
                  transformationVals.translateC.getDirection(), " axis by ",
                  transformationVals.translateC.getTranslVal())
        # --------------------------------------------SCALLING--------------------------------------------
        # SCALLING COMMAND FORMAT => S(AXIS)
        elif (len(instructString) >= 2
              and pygame.key.name(instructString[0]) == 's'):
            if checkKeys.isAlpha(instructString[1]):
                transformationVals.scaleC.setDirection(
                    pygame.key.name(instructString[1]))
                scaleVal = float(strManip.makeStr(instructString[2:]))
                transformationVals.scaleC.setScaleVal(scaleVal)
            else:
                scaleVal = float(strManip.makeStr(instructString[1:]))
                transformationVals.scaleC.setScaleVal(scaleVal)
                transformationVals.scaleC.setDirection()
            print("Scalling about ", transformationVals.scaleC.getDirection(),
                  "axis by", transformationVals.scaleC.getScaleVal())
        # --------------------------------------------EXTRUDE--------------------------------------------
        # EXTRUDE COMMAND FORMAT => T[]
        elif (pygame.key.name(instructString[0]) == 'e'):
            if (len(instructString) == 1):
                # set default val
                # omnidirectional scaling
                transformationVals.excrudeC.setDirection()
                transformationVals.excrudeC.setExtrudeVal()
            elif (len(instructString) >= 2 and checkKeys.isAxesAlpha(
                    pygame.key.name(instructString[1]))):
                # SET EXTRUDE DIR
                transformationVals.excrudeC.setDirection(
                    pygame.key.name(instructString[1]))
                if (len(instructString) > 2):
                    # get extrude val
                    extrudeVal = float(strManip.makeStr(instructString[2:]))
                    transformationVals.excrudeC.setExtrudeVal(extrudeVal)
                    pass
                else:
                    # default val
                    transformationVals.excrudeC.setExtrudeVal()
                    pass
            elif (checkKeys.isDigit(instructString[1])):
                # get extrude val
                extrudeVal = float(strManip.makeStr(instructString[1:]))
                transformationVals.excrudeC.setExtrudeVal(extrudeVal)
                # Set omnidirectional Extrude
                transformationVals.excrudeC.setDirection()
                pass
            print("Extrude along ", transformationVals.excrudeC.getDirection(),
                  "dir by", transformationVals.excrudeC.getExtrudeVal())

        # elif (len(instructString) >= 6
        #       and pygame.key.name(instructString[0]) == 'o'):
        #     OrgCoords = [x for x in strManip.getNumbers(instructString[1:])]

        #     transformationVals.originCoord = Coord(OrgCoords[0], OrgCoords[1],
        #                                            OrgCoords[2])

        #     print("Origin changed to:", "(", OrgCoords[0], ",", OrgCoords[1],
        #           ",", OrgCoords[2], ")")

    def processKey(self, eventKey):
        # print(eventKey, " = ", pygame.key.name(eventKey))

        # All Command instructions are aplhanumeric
        # 0 = 48 9 = 57 a= 97 z =122
        if (checkKeys.isAlpha(eventKey) or checkKeys.isDigit(eventKey)
                or eventKey == 44 or eventKey == 46):

            self.pressedKeys.append(eventKey)

        # Backspace key action
        if eventKey == pygame.K_BACKSPACE and len(self.pressedKeys) != 0:
            self.pressedKeys.pop()

        # Enter Key action
        elif eventKey == pygame.K_RETURN:
            # print(self.pressedKeys)
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
