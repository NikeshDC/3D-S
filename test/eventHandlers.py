from numpy.core.numeric import correlate
import pygame
from pygame import event

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

    def processInstruct(self,
                        instructString: list,
                        selected_surface=None,
                        mainCamera=None,
                        model=None):
        # Checking for transformation type
        # Length less than 2 causes index range error

        correct = True

        # --------------------------------------------ROTATION--------------------------------------------
        # ROTATION COMMAND FORMAT => R[AXIS][DEGREE]
        # Minimum command is r[dir](deg) deg is optional

        if pygame.key.name(instructString[0]) == 'r':
            count = 0
            if (len(instructString) < 2):
                correct = False
            elif (len(instructString) == 2) and checkKeys.isAlpha(
                    instructString[1]):
                correct = True
                if checkKeys.isAxesAlpha(pygame.key.name(instructString[1])):
                    transformationVals.rotateC.setDirection(
                        pygame.key.name(instructString[1]))
                else:
                    print("Invalid direction\nSelected Default Direction[x]")
                    transformationVals.rotateC.setDirection()
                # Setting Default angle
                transformationVals.rotateC.setAngle()
            else:
                correct = False
                if (pygame.key.name(instructString[2]) == '-'):
                    for x in instructString[3:]:
                        if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                                                      and count == 0):
                            correct = True
                            if (pygame.key.name(x) == '.'):
                                count = 1
                        else:
                            correct = False
                            break
                else:

                    for x in instructString[2:]:
                        if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                                                      and count == 0):
                            correct = True
                            if (pygame.key.name(x) == '.'):
                                count = 1
                        else:
                            correct = False
                            break

                if (correct):
                    if checkKeys.isAxesAlpha(pygame.key.name(
                            instructString[1])):
                        transformationVals.rotateC.setDirection(
                            pygame.key.name(instructString[1]))
                    else:
                        # print(
                        #     "Invalid direction\nSelected Default Direction[x]")
                        transformationVals.rotateC.setDirection()
                    rotationAngle = float(strManip.makeStr(instructString[2:]))
                    transformationVals.rotateC.setAngle(rotationAngle)
            if (correct):
                # print("Rotation about ",
                #       transformationVals.rotateC.getDirection(), " by ",
                #       transformationVals.rotateC.getAngle(), "degree")
                #rotating selected surface
                if selected_surface and mainCamera:
                    selected_surface.rotate_center(
                        transformationVals.rotateC.getAngle(),
                        transformationVals.rotateC.getDirection(), mainCamera)
            else:
                print("Invalid Instruction Format")

        # --------------------------------------------TRANSLATION--------------------------------------------
        # TRANSLATION COMMAND FORMAT => T[AXIS][VAL[DIST?]]

        elif (pygame.key.name(instructString[0]) == 't'):
            count = 0
            correct = False
            if (len(instructString) < 2):
                correct = False
            elif (len(instructString) == 2) and checkKeys.isAlpha(
                    instructString[1]):
                correct = True
                if (checkKeys.isAxesAlpha(pygame.key.name(instructString[1]))):
                    transformationVals.translateC.setDirection(
                        pygame.key.name(instructString[1]))
                else:
                    print("Invalid axis\nSelected Default axis[x]")
                    transformationVals.translateC.setDirection()
                # Setting Default Translation Value
                transformationVals.translateC.setTranslVal()
            else:  #ELIF LEN INS STR = MAX_PRECISION
                correct = False
                if (pygame.key.name(instructString[2]) == '-'):
                    for x in instructString[3:]:
                        if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                                                      and count == 0):
                            correct = True
                            if (pygame.key.name(x) == '.'):
                                count = 1
                        else:
                            correct = False
                            break
                else:

                    for x in instructString[2:]:
                        if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                                                      and count == 0):
                            correct = True
                            if (pygame.key.name(x) == '.'):
                                count = 1
                        else:
                            correct = False
                            break

                if (correct):
                    if (checkKeys.isAxesAlpha(
                            pygame.key.name(instructString[1]))):
                        transformationVals.translateC.setDirection(
                            pygame.key.name(instructString[1]))
                    else:
                        print("Invalid axis\nSelected Default axis[x]")
                        transformationVals.translateC.setDirection()
                    translationVal = float(strManip.makeStr(
                        instructString[2:]))
                    transformationVals.translateC.setTranslVal(translationVal)
            if (correct):
                # print("Translation in ",
                #       transformationVals.translateC.getDirection(),
                #       " axis by ",
                #       transformationVals.translateC.getTranslVal())
                #translating selected surface
                if selected_surface and mainCamera:
                    tx = 0
                    ty = 0
                    tz = 0
                    if transformationVals.translateC.getDirection() == 'x':
                        tx = transformationVals.translateC.getTranslVal()
                    elif transformationVals.translateC.getDirection() == 'y':
                        ty = transformationVals.translateC.getTranslVal()
                    elif transformationVals.translateC.getDirection() == 'z':
                        tz = transformationVals.translateC.getTranslVal()

                    selected_surface.translate(tx, ty, tz, mainCamera)
            else:
                print("Invalid Instruction Format")
        # --------------------------------------------SCALLING--------------------------------------------
        # SCALLING COMMAND FORMAT => S(AXIS)
        elif (pygame.key.name(instructString[0]) == 's'):
            count = 0
            correct = False
            if (len(instructString) < 2):
                correct = False
            else:
                # correct = True
                if (checkKeys.isAlpha(instructString[1])):
                    if (checkKeys.isAxesAlpha(
                            pygame.key.name(instructString[1]))):
                        transformationVals.scaleC.setDirection(
                            pygame.key.name(instructString[1]))
                    else:
                        print("Invalid axis\nSelected Default axis(Entirity)")
                        transformationVals.scaleC.setDirection()
                    correct = False
                    # for x in instructString[2:]:
                    #     if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                    #                                   and count == 0):
                    #         correct = True
                    #         if (pygame.key.name(x) == '.'):
                    #             count = 1
                    #     else:
                    #         correct = False
                    #         break
                    if (pygame.key.name(instructString[2]) == '-'):
                        for x in instructString[3:]:
                            if (checkKeys.isDigit(x)) or (
                                    pygame.key.name(x) == '.' and count == 0):
                                correct = True
                                if (pygame.key.name(x) == '.'):
                                    count = 1
                            else:
                                correct = False
                                break
                    else:

                        for x in instructString[2:]:
                            if (checkKeys.isDigit(x)) or (
                                    pygame.key.name(x) == '.' and count == 0):
                                correct = True
                                if (pygame.key.name(x) == '.'):
                                    count = 1
                            else:
                                correct = False
                                break

                    if (correct):
                        scaleVal = float(strManip.makeStr(instructString[2:]))
                        transformationVals.scaleC.setScaleVal(scaleVal)
                    elif (len(instructString) == 2):
                        correct = True
                        transformationVals.scaleC.setScaleVal()
                elif (checkKeys.isDigit(instructString[1])
                      or pygame.key.name(instructString[1]) == '-'):
                    correct = False
                    # for x in instructString[1:]:
                    #     if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                    #                                   and count == 0):
                    #         correct = True
                    #         if (pygame.key.name(x) == '.'):
                    #             count = 1
                    #     else:
                    #         correct = False
                    #         break
                    if (pygame.key.name(instructString[1]) == '-'):
                        for x in instructString[2:]:
                            if (checkKeys.isDigit(x)) or (
                                    pygame.key.name(x) == '.' and count == 0):
                                correct = True
                                if (pygame.key.name(x) == '.'):
                                    count = 1
                            else:
                                correct = False
                                break
                    else:

                        for x in instructString[1:]:
                            if (checkKeys.isDigit(x)) or (
                                    pygame.key.name(x) == '.' and count == 0):
                                correct = True
                                if (pygame.key.name(x) == '.'):
                                    count = 1
                            else:
                                correct = False
                                break

                    if (correct):
                        # Setting default direction
                        transformationVals.scaleC.setDirection()
                        scaleVal = float(strManip.makeStr(instructString[1:]))
                        transformationVals.scaleC.setScaleVal(scaleVal)
                else:
                    correct = False
            if (correct):
                # print("Scalling about ",
                #       transformationVals.scaleC.getDirection(), "axis by",
                #       transformationVals.scaleC.getScaleVal())
                #scaling selected surface
                if selected_surface and mainCamera:
                    sx = 1
                    sy = 1
                    sz = 1
                    if transformationVals.scaleC.getDirection() == 'x':
                        sx = transformationVals.scaleC.getScaleVal()
                    elif transformationVals.scaleC.getDirection() == 'y':
                        sy = transformationVals.scaleC.getScaleVal()
                    elif transformationVals.scaleC.getDirection() == 'z':
                        sz = transformationVals.scaleC.getScaleVal()
                    elif transformationVals.scaleC.getDirection() == 'a':
                        sx = transformationVals.scaleC.getScaleVal()
                        sy = transformationVals.scaleC.getScaleVal()
                        sz = transformationVals.scaleC.getScaleVal()

                    selected_surface.scale_center(sx, sy, sz, mainCamera)
            else:
                print("Invalid Instruction Format")
        # --------------------------------------------EXTRUDE--------------------------------------------
        # EXTRUDE COMMAND FORMAT => E(direction)(Value)
        elif (pygame.key.name(instructString[0]) == 'e'):
            count = 0
            correct = False
            if (len(instructString) == 1):
                correct = True
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
                    correct = False
                    # for x in instructString[2:]:
                    #     if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                    #                                   and count == 0):
                    #         correct = True
                    #         if (pygame.key.name(x) == '.'):
                    #             count = 1
                    #     else:
                    #         correct = False
                    #         break
                    if (pygame.key.name(instructString[2]) == '-'):
                        for x in instructString[3:]:
                            if (checkKeys.isDigit(x)) or (
                                    pygame.key.name(x) == '.' and count == 0):
                                correct = True
                                if (pygame.key.name(x) == '.'):
                                    count = 1
                            else:
                                correct = False
                                break
                    else:

                        for x in instructString[2:]:
                            if (checkKeys.isDigit(x)) or (
                                    pygame.key.name(x) == '.' and count == 0):
                                correct = True
                                if (pygame.key.name(x) == '.'):
                                    count = 1
                            else:
                                correct = False
                                break

                    if (correct):
                        # get extrude val
                        extrudeVal = float(strManip.makeStr(
                            instructString[2:]))
                        transformationVals.excrudeC.setExtrudeVal(extrudeVal)
                else:
                    correct = True
                    # default val
                    transformationVals.excrudeC.setExtrudeVal()
            elif (checkKeys.isDigit(instructString[1])
                  or pygame.key.name(instructString[1]) == '-'):
                correct = False
                # for x in instructString[1:]:
                #     if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                #                                   and count == 0):
                #         correct = True
                #         if (pygame.key.name(x) == '.'):
                #             count = 1
                #     else:
                #         correct = False
                #         break
                if (pygame.key.name(instructString[1]) == '-'):
                    for x in instructString[2:]:
                        if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                                                      and count == 0):
                            correct = True
                            if (pygame.key.name(x) == '.'):
                                count = 1
                        else:
                            correct = False
                            break
                else:

                    for x in instructString[1:]:
                        if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                                                      and count == 0):
                            correct = True
                            if (pygame.key.name(x) == '.'):
                                count = 1
                        else:
                            correct = False
                            break

                if (correct):
                    # get extrude val
                    extrudeVal = float(strManip.makeStr(instructString[1:]))
                    transformationVals.excrudeC.setExtrudeVal(extrudeVal)
                    # Set omnidirectional Extrude
                    transformationVals.excrudeC.setDirection()

            if (correct):
                # print("Extrude along ",
                #       transformationVals.excrudeC.getDirection(), "dir by",
                #       transformationVals.excrudeC.getExtrudeVal())
                if selected_surface and mainCamera and model:
                    model.extrude(selected_surface,
                                  transformationVals.excrudeC.getExtrudeVal(),
                                  transformationVals.excrudeC.getDirection(),
                                  mainCamera)
                    selected_surface = None
            else:
                print("Invalid Instruction Format")

        # --------------------------------------------INSSET--------------------------------------------
        # INSET COMMAND FORMAT => I(Value between min and max)
        elif (pygame.key.name(instructString[0]) == 'i'):
            count = 0
            correct = False
            if (len(instructString) == 1):
                correct = True
                # Setting Default Inset Value
                transformationVals.insetC.setInsetVal()
            elif (len(instructString) > 1):
                correct = False
                for x in instructString[1:]:
                    if (checkKeys.isDigit(x)) or (pygame.key.name(x) == '.'
                                                  and count == 0):
                        correct = True
                        if (pygame.key.name(x) == '.'):
                            count = 1
                    else:
                        correct = False
                        break
                if (correct):
                    # get inset val
                    insetVal = float(strManip.makeStr(instructString[1:]))
                    insetVal = InsetC.clamp(insetVal, InsetC.min, InsetC.max)
                    transformationVals.insetC.setInsetVal(insetVal)
            if (correct):
                #print("Inset by ", transformationVals.insetC.getInsetVal())
                if selected_surface and mainCamera and model:
                    model.inset(selected_surface, transformationVals.insetC.getInsetVal(), mainCamera)
                    selected_surface = None
            else:
                print("Invalid Instruction Format")


# -----------------------------------------------------------------------------------------------------------

    def changeToNum(self, eventKey, selected_surface, mainCamera, model):
        if (eventKey == 1073741922):
            # Numpad 0
            eventK = 48
        elif (eventKey == 1073741923):
            # Numpad period(.)
            eventK = 46
        elif (eventKey == 1073741910):
            # Numpad -
            eventK = 45
        elif (eventKey == 1073741912):
            if (len(self.pressedKeys) == 0):
                return
            # Enter Key
            self.processInstruct(self.pressedKeys, selected_surface,
                                 mainCamera, model)
            self.pressedKeys.clear()
            return
        elif (eventKey >= 1073741913 and eventKey <= 1073741921):
            # Numpad 1..9
            eventK = eventKey - 1073741864
        return eventK

    def processKey(self,
                   eventKey,
                   selected_surface=None,
                   mainCamera=None,
                   model=None):
        # print(eventKey, " = ", pygame.key.name(eventKey))

        # All Command instructions are aplhanumeric
        # 0 = 48 9 = 57 a= 97 z =122
        if (eventKey >= 1073741913 and eventKey <= 1073741923) or (
                eventKey == 1073741912) or (eventKey == 1073741910):
            eventK = self.changeToNum(eventKey, selected_surface, mainCamera,
                                      model)
            if (eventKey != 1073741912):
                self.pressedKeys.append(eventK)
        elif (checkKeys.isAlpha(eventKey) or checkKeys.isDigit(eventKey)
              or pygame.key.name(eventKey) == '.'
              or pygame.key.name(eventKey) == '-'):

            self.pressedKeys.append(eventKey)

        # Backspace key action
        elif eventKey == pygame.K_BACKSPACE and len(self.pressedKeys) != 0:
            self.pressedKeys.pop()

        # Enter Key action
        elif eventKey == pygame.K_RETURN and len(self.pressedKeys) != 0:
            # print(self.pressedKeys)
            self.processInstruct(self.pressedKeys, selected_surface,
                                 mainCamera, model)
            self.pressedKeys.clear()
        else:
            print("Unfamiliar Input Detected")

    def getRectCor(self):
        self.rect = self.commandWindow.getRect()

    def getPressedKeysStr(self):
        kStr = ''
        for x in self.pressedKeys:
            kStr = kStr + pygame.key.name(x)
        return kStr


class mouseScrollControl:
    def __init__(self,
                 initialList: list = [1, 2, 3, 4, 5, 6],
                 initialIndex=0,
                 THRES_X=300,
                 THRES_Y=300):
        self.selectedList = initialList
        self.selectedIndex = initialIndex
        self.movement = False
        self.movX = 0
        self.movY = 0
        self.THRES_X = THRES_X
        self.THRES_Y = THRES_Y

    def processEvent(self, event):
        if self.selectedList:
            if event.button == 4:
                # print("Scroll down")
                if (self.selectedIndex > 0):
                    self.selectedIndex = (self.selectedIndex - 1)
                else:
                    self.selectedIndex = len(self.selectedList) - 1
                # self.selectedList.pop()
                # self.selectedIndex = self.selectedList[-1]
            elif event.button == 5:
                # print("Scroll up")
                self.selectedIndex = (self.selectedIndex + 1) % len(
                    self.selectedList)
                # self.selectedList.append(self.selectedIndex)
            # print(self.selectedIndex)

    def setSelectedIndex(self, Index):
        self.selectedIndex = Index

    def getSelectedIndex(self):
        return self.selectedIndex

    def getSelectedList(self):
        return self.selectedList

    def processMovement(self, prevMouseX, prevMouseY, mouseX, mouseY):
        self.movX = mouseX - prevMouseX
        self.movY = mouseY - prevMouseY
        if (self.movX == self.movY == 0) or (self.movX > self.THRES_X
                                             or self.movY > self.THRES_Y):
            self.movement = False
            return
        else:
            self.movement = True

        # if (self.movX < 0):
        #     print("Right to left by ", -self.movX)
        # elif (self.movX > 0):
        #     print("Left to Right by ", self.movX)
        # else:
        #     print("No horizontal movement")
        # if (self.movY < 0):
        #     print("Bottom to Top by ", -self.movY)
        # elif (self.movY > 0):
        #     print("Top to Bottom by ", self.movY)
        # else:
        #     print("No vertital movement")


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
