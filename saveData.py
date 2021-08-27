from TransfClasses import Material
from pygame import Vector2, surface
from graphics_utility import Model, StandardModels, Surface, Vertex
from D3_utility import Camera


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

        python_file.write(
            repr(m1.material.color[0]) + "," + repr(m1.material.color[1]) +
            "," + repr(m1.material.color[2]) + "\n")
        python_file.write(
            repr(m1.material.ka) + "," + repr(m1.material.kd) + "," +
            repr(m1.material.ks) + "," + repr(m1.material.ns))
        python_file.close()
    except Exception as e:
        # print(e.__class__)
        status = False
    return status


def readModel(filename):
    try:
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
        materialColor = split(lines[-2], ",", int)
        materialVals = split(lines[-1], ",", float)
        print(materialColor, materialVals)
        model = Model()
        vertexObjL = []
        for vertex in vertexL:
            vertexObjL.append(Vertex(vertex[0], vertex[1], vertex[2]))

        for surface in vertexIndexForSurface:
            v1 = vertexObjL[surface[0]]
            v2 = vertexObjL[surface[1]]
            v3 = vertexObjL[surface[2]]

            s = Surface(v1, v2, v3)
            for i in range(3, len(surface)):
                v = vertexObjL[surface[i]]
                s.addVertex(v)

            model.addSurface(s)
        model.material.color = (materialColor[0], materialColor[1],
                                materialColor[2])
        model.material.ka = materialVals[0]
        model.material.kd = materialVals[1]
        model.material.ks = materialVals[2]
        model.material.ns = materialVals[3]
        return model
    except:
        pass
        return StandardModels().models['cube']


def saveAll(mainCamera: Camera):
    count = 0
    for model in mainCamera.models:
        if isinstance(model, Model):
            saveModel(model, str(count))
            count = count + 1


def readAll(mainCamera: Camera, count, begCount=0):

    for x in range(begCount, begCount + count):
        m = readModel(str(x))
        mainCamera.addModel(m)
        mainCamera.updateView()


# saveModel(StandardModels().models['cube'], "cube")
# readModel("cube")
