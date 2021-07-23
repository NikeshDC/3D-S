class checkKeys:
    def __init__(self) -> None:
        pass

    def isDigit(x):
        if x >= 48 and x <= 57:
            return True
        return False

    def isAlpha(x):
        if x >= 97 and x <= 122:
            return True
        return False

    def areDigits(self, strList: list):
        for x in strList:
            if (not self.isDigit(x)):
                return False
        return True


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


class rotateC:
    def __init__(self) -> None:
        # Default rotation is clockwise
        self.__rotateClockwise = True
        self.__degree = 0
        self.__fixedPoint = Coord()

    # True for clockwise and false for anticlockwise
    def setDirection(self, val: bool):
        self.__rotateClockwise = val

    def setAngle(self, deg):
        self.__degree = deg

    def setFixedPoint(self, xy: Coord):
        self.__fixedPoint = xy

    def getDirection(self):
        return self.__rotateClockwise

    def getAngle(self):
        return self.__degree

    def getFixedPoint(self):
        return self.__fixedPoint


class TransfVars:
    def __init__(self, rotateV=rotateC()) -> None:
        self.rotateC = rotateV
        # Classes not defined yet
        self.translateC = []
        self.scaleC = []
        self.excrudeC = []
