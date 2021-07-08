import math


class Vertex:
    '''class for representing vertex in a 3D-coordinate'''
    def __init__(self, x: float, y: float, z: float):
        self.x = x  #coordinate values of vertex
        self.y = y
        self.z = z

    def add(self, x: float, y: float, z: float):
        self.x += x
        self.y += y
        self.z += z

    def __add__(self, v):  #v is vertex
        return Vertex(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vertex(self.x - v.x, self.y - v.y, self.z - v.z)

    def __eq__(self, v):
        return ((self.x == v.x) and (self.y == v.y) and (self.z == v.z))

    def __ne__(self, v):
        return (self.x != v.x or self.y != v.y or self.z != v.z)


class Vector:
    '''class for representing vector in a 3D-coordinate'''
    def __init__(self, startVertex, endVertex):
        self.x = endVertex.x - startVertex.x
        self.y = endVertex.y - startVertex.y
        self.z = endVertex.z - startVertex.z


class Edge:
    '''class for representing edge in a 3D-coordinate'''
    def __init__(self, v1: Vertex, v2: Vertex):
        self.start = v1
        self.end = v2

    def getVector(self):
        return Vector(self.start, self.end)


class Surface:
    '''class for representing surface in a 3D-coordinate'''
    @staticmethod
    def getPlaneCoeffs(v1: Vertex, v2: Vertex, v3: Vertex):
        '''returns the coefficient A,B,C&D of the plane  Ax+By+Cz+D=0 represented by the vertices provided'''
        #(a,b,c) = (v2 - v1)cross(v3 - v1); d = -(a*v1.x + b*v1.y +c*v1.z)
        a = v1.y * (v2.z - v3.z) + v2.y * (v3.z - v1.z) + v3.y * (v1.z - v2.z)
        b = v1.z * (v2.x - v3.x) + v2.z * (v3.x - v1.x) + v3.z * (v1.x - v2.x)
        c = v1.x * (v2.y - v3.y) + v2.x * (v3.y - v1.y) + v3.x * (v1.y - v2.y)
        d = -v1.x * (v2.y * v3.z - v3.y * v2.z) - v2.x * (
            v3.y * v1.z - v1.y * v3.z) - v3.x * (v1.y * v2.z - v2.y * v1.z)
        return (a, b, c, d)

    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex):
        '''makes surface from 3 vertices specified in conterclockwise direction with respect to required normal'''
        e1 = Edge(v1, v2)
        e2 = Edge(v2, v3)
        e3 = Edge(v3, v1)
        self.edges = [e1, e2, e3]
        self.a, self.b, self.c, self.d = Surface.getPlaneCoeffs(v1, v2, v3)
        self.vertices = [v1, v2, v3]

    def addVertex(self, v):
        #v = projection of v on plane made by first three vertices
        a, b, c, d = self.a, self.b, self.c, self.d
        t = -(a * v.x + b * v.y + c * v.z + d) / math.sqrt(a * a + b * b +
                                                           c * c)
        newv = Vertex(0, 0, 0)
        newv.x, newv.y, newv.z = a * t + v.x, b * t + v.y, c * t + v.z
        if not (newv == v):
            print(
                f"vertex not lying in plane vertex:({v.x},{v.y},{v.z})  \nprojection:({newv.x},{newv.y},{newv.z})"
            )
            return
        if v in self.vertices:
            print("vertex already included in surface")
            return

        vend = self.edges[-1].end
        vstart = self.edges[-1].start
        self.edges.pop(
        )  #removing last edge to make new edges connecting to the new vertex
        self.edges.append(Edge(vstart, v))
        self.edges.append(Edge(v, vend))
        self.vertices.append(v)


class Model:
    '''class for representing a object in a 3D-coordinate'''
    def __init__(self):
        self.surfaces = []
        self.vertices = []

    def addSurface(self, s: Surface):
        self.surfaces.append(s)
        for vertex in s.vertices:
            if not vertex in self.vertices:
                self.vertices.append(vertex)


class StandardModels:
    def __init__(self):
        '''class to contain the standard in-built models avialable for 3d-modeling'''
        self.models = {}

        ## ------ cube ------ ##
        cube = Model()
        v1 = Vertex(0.0, 0.0, 0.0)
        v2 = Vertex(1.0, 0.0, 0.0)
        v3 = Vertex(1.0, 1.0, 0.0)
        v4 = Vertex(0.0, 1.0, 0.0)
        v5 = Vertex(0.0, 1.0, 1.0)
        v6 = Vertex(0.0, 0.0, 1.0)
        v7 = Vertex(1.0, 0.0, 1.0)
        v8 = Vertex(1.0, 1.0, 1.0)
        s1 = Surface(v1, v2, v3)
        s1.addVertex(v4)
        s2 = Surface(v1, v6, v5)
        s2.addVertex(v4)
        s3 = Surface(v5, v6, v7)
        s3.addVertex(v8)
        s4 = Surface(v8, v7, v2)
        s4.addVertex(v3)
        s5 = Surface(v4, v5, v8)
        s5.addVertex(v3)
        s6 = Surface(v1, v2, v7)
        s6.addVertex(v6)
        cube.addSurface(s2)
        cube.addSurface(s1)
        cube.addSurface(s6)
        cube.addSurface(s3)
        ##        cube.addSurface(s4)
        ##        cube.addSurface(s5)

        self.models['cube'] = cube
        ## ------------------ ##


class Grid:
    '''class to create a grid spanning on xz-plane'''
    def __init__(self, gridspacing, span, grid_color, xaxis_color,
                 zaxis_color):
        self.edges = []
        self.vertices = []
        self.grid_color = grid_color
        self.xaxis_color = xaxis_color
        self.zaxis_color = zaxis_color

        self.xaxis = Edge(Vertex(-span, 0, 0), Vertex(span, 0, 0))
        self.zaxis = Edge(Vertex(0, 0, -span), Vertex(0, 0, span))
        curspan = gridspacing
        while curspan < span:
            edge1 = Edge(Vertex(-span, 0, curspan), Vertex(span, 0, curspan))
            edge2 = Edge(Vertex(-span, 0, -curspan), Vertex(span, 0, -curspan))
            edge3 = Edge(Vertex(curspan, 0, -span), Vertex(curspan, 0, span))
            edge4 = Edge(Vertex(-curspan, 0, -span), Vertex(-curspan, 0, span))
            self.edges.append(edge1)
            self.edges.append(edge2)
            self.edges.append(edge3)
            self.edges.append(edge4)
            curspan += gridspacing
