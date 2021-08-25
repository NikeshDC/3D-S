from graphics_utility import *
import numpy

screen_x, screen_y = 1100, 700
screen_xy = min(screen_x, screen_y)

screen_yc = screen_y - 5


def topixel(x, y):
    '''converts normalized value to actual pixel values'''
    x = int((screen_x + x * screen_xy) / 2)
    y = int((screen_y + y * screen_xy) / 2)
    return (x, y)


class ZBuff:
    depthBuff = []
    refBuff = []
    # iniDepth, iniInt = 100, 1
    row = []

    def initializeDepthAndRefBuffer(self):
        for x in range(screen_x):
            rowD = [self.iniDepth for x in range(screen_y)]
            rowI = [self.iniInt for x in range(screen_y)]
            self.depthBuff.append(rowD)
            self.refBuff.append(rowI)
        pass
        # print(self.depthBuff, self.refBuff)

    def __init__(self, iniDepthV=1, iniIntV=(255, 255, 255)) -> None:
        self.iniDepth = iniDepthV
        self.iniInt = iniIntV
        self.initializeDepthAndRefBuffer()
        pass

    def calcZVal(z, a, c):
        return z - (a / c)

    def ZBuffCalc(self, m1: Model = Model()):
        for surface in m1.surfaces:
            # processedV = []
            xList = []
            yList = []
            for i in range(len(surface.vertices)):
                x, y = topixel(surface.vertices[i].vx, surface.vertices[i].vy)
                xList.append(x)
                yList.append(y)
            # pixInd = numpy.argmin(yList)
            pixXStart, pixYStart = numpy.argmin(xList), numpy.argmin(yList)
            pixXEnd, pixYEnd = numpy.argmax(xList), numpy.argmax(yList)
            a, b, c, d = Surface.getPlaneCoeffs(surface.vertices[0],
                                                surface.vertices[1],
                                                surface.vertices[2])
            # zVal = (((-a) * x) - (b * y) - d) / c
            # zVal =
            for pixY in range(pixYStart, pixYEnd):
                for pixX in range(pixXStart, pixXEnd):
                    print(pixX, pixY)
                    zVal = self.calcZVal(zVal, a, c)
                    if self.depthBuff[pixX][pixY] < zVal:
                        self.depthBuff[pixX][pixY] = zVal
                        # change color
                        self.refBuff[pixX][pixY] = (1, 1, 1)
                        pass
                # print("heyy", x, y)
            # print("---------------")
            pass
        pass