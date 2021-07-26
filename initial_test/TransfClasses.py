class checkKeys:
    def __init__(self) -> None:
        pass

    @staticmethod
    def isDigit(x):
        if x >= 48 and x <= 57:
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
    defaultVal, defaultDir = 90.0, 'x'

    def __init__(self, dir=defaultDir, deg=defaultVal) -> None:
        # Default rotation is clockwise
        self.__rotateDir = dir
        self.__degree = deg
        self.__fixedPoint = Coord()

    # True for clockwise and false for anticlockwise
    def setDirection(self, dir):
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

    def setDirection(self, dir):
        self.__translDir = dir

    def getTranslVal(self):
        return self.__translVal

    def getDirection(self):
        return self.__translDir


class ScaleC:
    defaultVal, defaultDir = 2.0, 'x'

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
    defaultVal, defaultDir = 1.0, 'a'

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


class TransfVars:
    def __init__(
        self,
        rotateV=RotateC(),
        translateV=TranslateC(),
        scaleV=ScaleC(),
        extrudeV=ExtrudeC(),
        originV=Coord()
    ) -> None:

        self.rotateC = rotateV
        self.originCoord = originV

        self.translateC = translateV
        self.scaleC = scaleV
        # Classes not defined yet
        self.excrudeC = extrudeV


def selectAll():
    # Select all edges
    print("All edges selected.")
    pass