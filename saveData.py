from pygame import Vector2, surface
from graphics_utility import Model, Surface, Vertex


def split(NStri, separator=",", type=float):
    separatedList = []
    item = ""
    for x in NStri:
        if (x == separator):
            indItem = type(item)
            separatedList.append(indItem)
            # Clearing previous item
            item = ""
            continue
        item = item + x
    # Extracting last item
    lastItem = type(item)
    separatedList.append(lastItem)
    return separatedList


def saveModel(m1: Model, filename):
    status = True
    indexList = []
    try:
        python_file = open(filename + ".txt", "w")
        surfaceList = [x for x in m1.surfaces]
        edgeList = [x for x in m1.edges]
        vertexList = [x for x in m1.vertices]
        lengthV = repr(len(vertexList))
        python_file.write(lengthV + "\n")
        for vertex in vertexList:
            x = repr(vertex.x)
            y = repr(vertex.y)
            z = repr(vertex.z)
            python_file.write(x + "," + y + "," + z + "\n")

        for surface in surfaceList:
            iList = []
            for x in range(len(surface.vertices)):
                iList.append(vertexList.index(surface.vertices[x]))
                pass
            indList = [x for x in iList]
            indexList.append(indList)

        lengthI = repr(len(indexList))
        python_file.write(lengthI + "\n")
        for x in indexList:
            for y in range(len(x)):
                a = repr(x[y])
                # print(x)
                if (y == len(x) - 1):
                    python_file.write(a + "\n")
                    continue
                python_file.write(a + ",")

        python_file.close()
    except Exception as e:
        # print(e.__class__)
        status = False
    return status


def readModel(filename):
    p_file = open(filename + ".txt", "r")
    lines = p_file.readlines()

    lenVertexList = int(lines[0])
    lenSurfaceList = int(lines[lenVertexList + 1])

    # Vertex co-ordinates
    vertexL = []
    for i in range(1, lenVertexList + 1):
        vertexL.append(split(lines[i], ","))

    # Surface-wise Vertex indices
    vertexIndexForSurface = []
    for i in range(lenVertexList + 2, lenVertexList + lenSurfaceList + 2):
        vertexIndexForSurface.append(split(lines[i], ",", int))

    model = Model()
    ind = 0
    for surface in vertexIndexForSurface:
        ind = ind + 1
        v1 = Vertex(vertexL[surface[0]][0], vertexL[surface[0]][1],
                    vertexL[surface[0]][2])
        v2 = Vertex(vertexL[surface[1]][0], vertexL[surface[1]][1],
                    vertexL[surface[1]][2])
        v3 = Vertex(vertexL[surface[2]][0], vertexL[surface[2]][1],
                    vertexL[surface[2]][2])

        s = Surface(v1, v2, v3)
        for i in range(3, len(surface)):
            v = Vertex(vertexL[surface[i]][0], vertexL[surface[i]][1],
                       vertexL[surface[i]][2])
            s.addVertex(v)
        # TEST --------To check individual surfaces
        # if (ind == 17):
        model.addSurface(s)

    # TEST --------To check individual surfaces
    # surface = vertexIndexForSurface[0]
    # v1 = Vertex(vertexL[surface[0]][0], vertexL[surface[0]][1],
    #             vertexL[surface[0]][2])
    # v2 = Vertex(vertexL[surface[1]][0], vertexL[surface[1]][1],
    #             vertexL[surface[1]][2])
    # # v2 = Vertex(0.0, 1.0, 0.0)
    # v3 = Vertex(vertexL[surface[2]][0], vertexL[surface[2]][1],
    #             vertexL[surface[2]][2])
    # v4 = Vertex(vertexL[surface[3]][0], vertexL[surface[3]][1],
    #             vertexL[surface[3]][2])
    # s = Surface(v1, v2, v3)
    # s.addVertex(v4)
    # model.addSurface(s)

    return model


# print(saveModel(Model(), "Sample"))
#readModel("sample")
