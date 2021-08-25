class checkKeys:
    def __init__(self) -> None:
        pass

    @staticmethod
    def isDigit(x):
        if (x >= 48 and x <= 57):  #or (x >= 1073741913 and x <= 1073741922):
            return True
        return False

    @staticmethod
    def isAlpha(x):
        if x >= 97 and x <= 122:
            return True
        return False

    @staticmethod
    def areDigits(self, strList: list):
        for x in strList:
            if (not self.isDigit(x)):
                return False
        return True

    def isAxesAlpha(char):
        if char == 'x' or char == 'y' or char == 'z':
            return True
        return False


from collections import defaultdict
from graphics_utility import StandardModels
from typing import DefaultDict
import pygame


class strManip:
    def __init__(self) -> None:
        pass

    @staticmethod
    def getNumbers(ipString: list, separator=",") -> list:
        ans = []
        temp = 0
        for x in ipString:
            if (checkKeys.isDigit(x)):
                temp = temp * 10 + int(pygame.key.name(x))

            elif (pygame.key.name(x) == separator):
                ans.append(temp)
                temp = 0
        ans.append(temp)
        return ans

    @staticmethod
    def makeStr(li: list):
        stri = ""
        for x in li:
            stri = stri + pygame.key.name(x)
        return stri


class Coord:
    def __init__(self, px=0, py=0, pz=0) -> None:
        self.__x = px
        self.__y = py
        self.__z = pz

    def setX(self, CX):
        self.__x = CX

    def setX(self, CY):
        self.__y = CY

    def setZ(self, CZ):
        self.__z = CZ

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getZ(self):
        return self.__z


class RotateC:
    defaultVal, defaultDir = 90.0, 'y'

    def __init__(self, dir=defaultDir, deg=defaultVal) -> None:
        # Default rotation is clockwise
        self.__rotateDir = dir
        self.__degree = deg
        self.__fixedPoint = Coord()

    # True for clockwise and false for anticlockwise
    def setDirection(self, dir=defaultDir):
        self.__rotateDir = dir

    def setAngle(self, deg=defaultVal):
        self.__degree = deg

    def setFixedPoint(self, xy: Coord):
        self.__fixedPoint = xy

    def getDirection(self):
        return self.__rotateDir

    def getAngle(self):
        return self.__degree

    def getFixedPoint(self):
        return self.__fixedPoint


class TranslateC:
    defaultVal, defaultDir = 1.0, 'x'

    def __init__(self, translationValue=defaultVal, dir=defaultDir) -> None:
        self.__translVal = translationValue
        self.__translDir = dir

    def setTranslVal(self, val: float = defaultVal):
        self.__translVal = val

    def setDirection(self, dir=defaultDir):
        self.__translDir = dir

    def getTranslVal(self):
        return self.__translVal

    def getDirection(self):
        return self.__translDir


class ScaleC:
    defaultVal, defaultDir = 2.0, 'a'

    def __init__(self, scalingValue=defaultVal, dir=defaultDir) -> None:
        self.__scaleVal = scalingValue
        self.__scaleDir = dir

    def setScaleVal(self, val: float = defaultVal):
        self.__scaleVal = val

    def setDirection(self, dir=defaultDir):
        self.__scaleDir = dir

    def getScaleVal(self):
        return self.__scaleVal

    def getDirection(self):
        return self.__scaleDir


class ExtrudeC:
    defaultVal, defaultDir = 1.0, 'n'

    def __init__(self, extrudingValue=defaultVal, dir=defaultDir) -> None:
        self.__extrudeVal = extrudingValue
        self.__extrudeDir = dir

    def setExtrudeVal(self, val: float = defaultVal):
        self.__extrudeVal = val

    def setDirection(self, dir=defaultDir):
        self.__extrudeDir = dir

    def getExtrudeVal(self):
        return self.__extrudeVal

    def getDirection(self):
        return self.__extrudeDir


class InsetC:
    defaultVal = 0.5
    min, max = 0.05, 0.95

    def __init__(self, insettingValue=defaultVal) -> None:
        self.__insetVal = insettingValue

    def setInsetVal(self, val: float = defaultVal):
        self.__insetVal = val

    def getInsetVal(self):
        return self.__insetVal

    def clamp(val, minV=min, maxV=max):
        if (val < minV):
            return minV
        elif (val > maxV):
            return maxV
        return val


class TransfVars:
    def __init__(
        self,
        rotateV=RotateC(),
        translateV=TranslateC(),
        scaleV=ScaleC(),
        extrudeV=ExtrudeC(),
        insetV=InsetC(),
        LRotateV=RotateC(),
        LTranslateV=TranslateC(),
        originV=Coord()
    ) -> None:

        self.rotateC = rotateV
        self.translateC = translateV
        self.scaleC = scaleV
        self.excrudeC = extrudeV
        self.insetC = insetV
        self.LRotateC = LRotateV
        self.LTranslateC = LTranslateV

        self.originCoord = originV


class Material:
    defaultSpecRadius = 1
    defaultColor = (0, 0, 0)
    defaultSpecConstant = 1
    defaultAmbient = 1
    defaultDiffuse = 1

    def __init__(self,
                 rgbV=defaultColor,
                 specRadiusV=defaultSpecRadius,
                 specConstantV=defaultSpecConstant,
                 ambientV=defaultAmbient,
                 diffuseV=defaultDiffuse) -> None:
        self.color = rgbV
        self.specConstant = specConstantV
        self.specRadius = specRadiusV
        self.ambient = ambientV
        self.diffuse = diffuseV
        pass


def selectAll():
    # Select all edges
    print("All edges selected.")
    pass


# Origins
ORIGIN, CENTRE = 0, 1


def changeOrigin(orginSel: bool):
    # Code to toogle origin
    if orginSel == ORIGIN:
        # Set origin to main origin
        print("Main")
        orginSel = CENTRE
        pass
    elif orginSel == CENTRE:
        # Set origin to object's centre
        print("Centre")
        orginSel = ORIGIN
        pass
    # orginSel = orginSel + 1
    return orginSel


def createNewModel() -> StandardModels:
    print("Create New Model")
    m = StandardModels().model['cube']
    return m
    pass