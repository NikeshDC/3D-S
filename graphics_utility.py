import math
#from D3_utility import Camera, Transform_matrix
#from utility_2d import isInterior
import copy
import pygame
from settings import Window, Shading
import numpy

##screen_x = 1100
##screen_y = 700
###account for different dimensions of screen width and height to draw proportionately
##screen_xy = min(screen_x,screen_y)
##line_color = (241,165,5)


def topixelx(x):
    '''converts normalized x-axis value to actual pixel values'''
    x = int((Window.width + x * Window.xy) / 2)
    return x


def topixely(y):
    '''converts normalized y-axis value to actual pixel values'''
    y = int((Window.height - y * Window.xy) / 2)
    return y


def topixel(x, y):
    '''converts normalized value to actual pixel values'''
    x = int((Window.width + x * Window.xy) / 2)
    y = int((Window.height - y * Window.xy) / 2)
    return (x, y)


def tonormal(x, y):
    '''converts pixel value to normalized value'''
    x = float((2 * x - Window.width) / Window.xy)
    y = float((-2 * y + Window.height) / Window.xy)
    return (x, y)


class Transform_matrix:
    @staticmethod
    def translate(tx: float, ty: float, tz: float):
        '''returns 4x4 matrix for 3D translation based on parameters specified'''
        return numpy.array([[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz],
                            [0, 0, 0, 1]])

    @staticmethod
    def scale(sx: float, sy: float, sz: float):
        '''returns 4x4 matrix for 3D translation based on parameters specified'''
        return numpy.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0],
                            [0, 0, 0, 1]])

    @staticmethod
    def rotate(angle: float, axis):
        '''returns 4x4 matrix for 3D translation based on angle(in degrees) and axis specified'''
        angle = angle / 180 * math.pi
        if axis == 'x':
            return numpy.array([[1, 0, 0, 0],
                                [0, math.cos(angle), -math.sin(angle), 0],
                                [0, math.sin(angle),
                                 math.cos(angle), 0], [0, 0, 0, 1]])
        elif axis == 'y':
            return numpy.array([[math.cos(angle), 0,
                                 math.sin(angle), 0], [0, 1, 0, 0],
                                [-math.sin(angle), 0,
                                 math.cos(angle), 0], [0, 0, 0, 1]])
        elif axis == 'z':
            return numpy.array([[math.cos(angle),
                                 math.sin(angle), 0, 0],
                                [-math.sin(angle),
                                 math.cos(angle), 0, 0], [0, 0, 1, 0],
                                [0, 0, 0, 1]])

    @staticmethod
    def transform(vertex, tm):
        v = numpy.array([[vertex.x], [vertex.y], [vertex.z], [1]])
        v = tm.dot(v)
        vertex.x, vertex.y, vertex.z = v[0][0], v[1][0], v[2][0]


class Material:
    '''defines the maretial properties for surface'''
    def __init__(self, color=(255, 255, 255), ka=1.0, kd=1.0, ks=1.0, ns=10):
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.ns = ns

    def setColor(self, r=0, g=0, b=0):
        self.color = (r, g, b)

    def setKa(self, kaV=0):
        self.ka = kaV

    def setKd(self, kdV=0):
        self.kd = kdV

    def setKs(self, ksV=0):
        self.ks = ksV

    def setNs(self, nsV=0):
        self.ns = nsV


class Vertex:
    '''class for representing vertex in a 3D-coordinate'''
    def __init__(self, x: float, y: float, z: float, TOL=10):
        self.x = x  #coordinate values of vertex in world view
        self.y = y
        self.z = z
        self.TOL = TOL  #vertex coordinates equal to TOL decimal places are considered equal

        #coordinate values of vertices for viewing co-ordinate/ or perspective viewing
        self.vx = x
        self.vy = y
        self.vz = z

        self.intensity = 0.0
        self.normal = [0.0, 0.0, 0.0]  #average normal of associated surfaces

        self.transformed = False
        self.associated_surfaces = 0

    def __eq__(self, v):
        #return ((self.x == v.x) and (self.y == v.y) and (self.z == v.z))
        return (round(self.x, self.TOL) == round(v.x, self.TOL)) and (round(
            self.y, self.TOL) == round(v.y, self.TOL)) and (round(
                self.z, self.TOL) == round(v.z, self.TOL))

    def __ne__(self, v):
        #return (self.x != v.x or self.y != v.y or self.z != v.z)
        return (round(self.x, self.TOL) != round(v.x, self.TOL)
                or round(self.y, self.TOL) != round(v.y, self.TOL)
                or round(self.z, self.TOL) != round(v.z, self.TOL))

    def addAssociatedSurface(self, surface):
        a = surface.a + self.associated_surfaces * self.normal[0]
        b = surface.b + self.associated_surfaces * self.normal[1]
        c = surface.c + self.associated_surfaces * self.normal[2]
        self.associated_surfaces += 1
        self.normal[0] = a / self.associated_surfaces
        self.normal[1] = b / self.associated_surfaces
        self.normal[2] = c / self.associated_surfaces

    def removeAssociatedSurface(self, surface):
        if (self.associated_surfaces < 1):
            print("associated surfaces zero")
            return
        self.associated_surfaces -= 1


class Edge:
    '''class for representing edge in a 3D-coordinate'''
    def __init__(self, v1: Vertex, v2: Vertex):
        self.start = v1
        self.end = v2

    def setViewingSlope(self):
        dx = (self.end.vx - self.start.vx)
        dy = (self.end.vy - self.start.vy)
        if dx == 0:
            self.m = math.inf
            self.m_inv = 0
            return
        elif dy == 0:
            self.m = 0
            self.m_inv = math.inf
            return

        self.m = dy / dx
        self.m_inv = dx / dy


class Surface:
    '''class for representing surface in a 3D-coordinate'''
    @staticmethod
    def getPlaneCoeffs(v1: Vertex, v2: Vertex, v3: Vertex):
        '''returns the coefficient A,B,C&D of the plane  Ax+By+Cz+D=0 represented by the vertices provided'''
        #(a,b,c) = (v2 - v1)cross(v3 - v1); d = -(a*v1.x + b*v1.y +c*v1.z)
        a = (v1.y * (v2.z - v3.z) + v2.y * (v3.z - v1.z) + v3.y *
             (v1.z - v2.z))
        b = (v1.z * (v2.x - v3.x) + v2.z * (v3.x - v1.x) + v3.z *
             (v1.x - v2.x))
        c = (v1.x * (v2.y - v3.y) + v2.x * (v3.y - v1.y) + v3.x *
             (v1.y - v2.y))
        #d = (-v1.x*(v2.y*v3.z - v3.y*v2.z) - v2.x*(v3.y*v1.z - v1.y*v3.z) - v3.x*(v1.y*v2.z - v2.y*v1.z))
        d = -(a * v1.x + b * v1.y + c * v1.z)
        norm_abs = math.sqrt(a * a + b * b + c * c)
        a, b, c, d = a / norm_abs, b / norm_abs, c / norm_abs, d / norm_abs  #normalizing to get normal vectors
        #print("a:",a," b:",b," c:",c," d:",d)
        return (a, b, c, d)

    def setPlaneCoeffs(self):
        self.a, self.b, self.c, self.d = Surface.getPlaneCoeffs(
            self.vertices[0], self.vertices[1], self.vertices[2])

    def calcMinMaxViews(self):
        self.min_vx = self.vertices[0].vx
        self.max_vx = self.vertices[0].vx
        self.min_vy = self.vertices[0].vy
        self.max_vy = self.vertices[0].vy
        #calculating minimum and maximum viewing coordinate values
        for vertex in self.vertices:
            if vertex.vx < self.min_vx:
                self.min_vx = vertex.vx
            if vertex.vx > self.max_vx:
                self.max_vx = vertex.vx
            if vertex.vy < self.min_vy:
                self.min_vy = vertex.vy
            if vertex.vy > self.max_vy:
                self.max_vy = vertex.vy
        #print(self.min_vx, self.max_vx, self.min_vy, self.max_vy)

    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, material=None):
        '''makes surface from 3 vertices specified in conterclockwise direction with respect to required normal'''
        e1 = Edge(v1, v2)
        e2 = Edge(v2, v3)
        e3 = Edge(v3, v1)
        self.edges = [e1, e2, e3]
        self.a, self.b, self.c, self.d = Surface.getPlaneCoeffs(v1, v2, v3)
        self.vertices = [v1, v2, v3]
        self.center = Vertex((v1.x + v2.x + v3.x) / 3,
                             (v1.y + v2.y + v3.y) / 3,
                             (v1.z + v2.z + v3.z) / 3)
        self.material = material
        self.backface = False

    def addVertex(self, v):
        #v = projection of v on plane made by first three vertices
        a, b, c, d = self.a, self.b, self.c, self.d
        #t = -(a*v.x + b*v.y + c*v.z + d)/math.sqrt(a*a + b*b + c*c) ;already normalized (math.sqrt(a*a + b*b + c*c) = 1)
        t = -(a * v.x + b * v.y + c * v.z + d)
        projv = Vertex(0, 0, 0)
        projv.x, projv.y, projv.z = a * t + v.x, b * t + v.y, c * t + v.z
        if not (projv == v):
            print(
                f"vertex not lying in plane vertex:({v.x},{v.y},{v.z})  \nprojection:({projv.x},{projv.y},{projv.z})"
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
        n = len(self.vertices)
        self.center = Vertex((self.center.x * n + v.x) / (n + 1),
                             (self.center.y * n + v.y) / (n + 1),
                             (self.center.z * n + v.z) / (n + 1))
        self.vertices.append(v)

    def setCenter(self):
        center_x, center_y, center_z = 0, 0, 0
        for vertex in self.vertices:
            center_x += vertex.x
            center_y += vertex.y
            center_z += vertex.z
        vn = len(self.vertices)
        self.center.x = center_x / vn  #centroid
        self.center.y = center_y / vn
        self.center.z = center_z / vn

    def setTransformed(self):
        for vertex in self.vertices:
            vertex.transformed = True

    def translate(self, tx, ty, tz, camera):
        for vertex in self.vertices:
            vertex.x += tx
            vertex.y += ty
            vertex.z += tz
        camera.setViewingValues(self.vertices)
        self.setTransformed()

##            v = numpy.array([[vertex.x],
##                             [vertex.y],
##                             [vertex.z],
##                             [1       ]])
##            v = camera.W2Vm.dot(v)
##
##            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
##            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
##            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def rotate(self, angle, axis, camera):
        '''rotate about given axis('x' / 'y' / 'z') with world origin as fixed point'''
        rm = Transform_matrix.rotate(angle, axis)
        camera.setViewingValues(self.vertices, rm)
        self.setTransformed()
##        for vertex in self.vertices:
##            v = numpy.array([[vertex.x],
##                             [vertex.y],
##                             [vertex.z],
##                             [1       ]])
##            v = rm.dot(v)
##            vertex.x, vertex.y, vertex.z = v [0], v[1], v[2]
##
##            v = camera.W2Vm.dot(v)
##            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
##            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
##            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def rotate_center(self, angle, axis, camera):
        '''rotate about given axis('x' / 'y' / 'z') with center of the surface as fixed point'''
        self.rotateFP(self.center.x, self.center.y, self.center.z, angle, axis,
                      camera)
##        center_x, center_y, center_z = 0.0, 0.0, 0.0
##        for vertex in self.vertices:
##            center_x += vertex.x
##            center_y += vertex.y
##            center_z += vertex.z
##        vn = len(self.vertices)
##        center_x /= vn     #centroid
##        center_y /= vn
##        center_z /= vn
##        self.rotateFP(self.center.x, self.center.y, self.center.z, angle, axis, camera)

    def rotateFP(self, fx, fy, fz, angle, axis, camera):
        '''rotate the surface about fixed point about given axis('x' / 'y' / 'z') about fixed point'''
        #checking if rotation doesnot cause the vertices to lie outside for other surfaces i.e. rotation is only possible about line lying in/parallel to this surface
        #here checking perpendicularity of normal of the surface to the rotation axis (i.e. rotation axis is parallel to plane)
        if axis == 'x':
            if self.a != 0:
                print("cant roatate about x-axis")
                return
        elif axis == 'y':
            if self.b != 0:
                print("cant roatate about y-axis")
                return
        elif axis == 'z':
            if self.c != 0:
                print("cant roatate about z-axis")
                return
        else:
            return

        tm1 = Transform_matrix.translate(-fx, -fy, -fz)
        rm = Transform_matrix.rotate(angle, axis)
        tm2 = Transform_matrix.translate(fx, fy, fz)
        rm = tm2.dot(rm.dot(tm1))  #composite rotation matrix
        camera.setViewingValues(self.vertices, rm)
        self.setTransformed()
##        for vertex in self.vertices:
##            v = numpy.array([[vertex.x],
##                             [vertex.y],
##                             [vertex.z],
##                             [1       ]])
##            v = rm.dot(v)
##            vertex.x, vertex.y, vertex.z = v [0][0], v[1][0], v[2][0]
##
##            v = camera.W2Vm.dot(v)
##            vertex.vx, vertex.vy, vertex.vz = v [0][0], v[1][0], v[2][0]
##            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
##            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def scale(self, sx, sy, sz, camera):
        for vertex in self.vertices:
            vertex.x *= sx
            vertex.y *= sy
            vertex.z *= sz
        camera.setViewingValues(self.vertices)
        self.setTransformed()


##            v = numpy.array([[vertex.x],
##                             [vertex.y],
##                             [vertex.z],
##                             [1       ]])
##            v = camera.W2Vm.dot(v)
##            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
##            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
##            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def scale_center(self, sx, sy, sz, camera):
        '''scale about center of the surface as fixed point'''
        self.scaleFP(self.center.x, self.center.y, self.center.z, sx, sy, sz,
                     camera)

    def scaleFP(self, fx, fy, fz, sx, sy, sz, camera):
        '''rotate the surface about fixed point about given axis('x' / 'y' / 'z') about fixed point'''
        tm1 = Transform_matrix.translate(-fx, -fy, -fz)
        sm = Transform_matrix.scale(sx, sy, sz)
        tm2 = Transform_matrix.translate(fx, fy, fz)
        sm = tm2.dot(sm.dot(tm1))  #composite scaling matrix
        camera.setViewingValues(self.vertices, sm)
        self.setTransformed()


class Model:
    '''class for representing a object in a 3D-coordinate'''
    def __init__(self, wireframeColor=(241, 165, 5), shading=Shading.FLAT):
        self.surfaces = []
        self.vertices = []
        self.edges = []
        self.wireframeColor = wireframeColor
        self.wireframe = True
        self.material = Material()
        self.active = True
        self.shading = shading

    def addSurface(self, s: Surface):
        self.surfaces.append(s)
        for vertex in s.vertices:
            if not vertex in self.vertices:
                self.vertices.append(vertex)
        for edge in s.edges:
            if not edge in self.edges:
                self.edges.append(edge)

    def setVertexNormals(self):
        for vertex in self.vertices:
            a, b, c = 0.0, 0.0, 0.0
            for surface in self.surfaces:
                if vertex in surface.vertices:
                    a += surface.a
                    b += surface.b
                    c += surface.c
            norm = math.sqrt(a * a + b * b + c * c)
            a, b, c = a / norm, b / norm, c / norm
            vertex.normal = (a, b, c)

    def calcMinMaxViews(self):
        for surface in self.surfaces:
            surface.calcMinMaxViews()
        for edge in self.edges:
            edge.setViewingSlope()

    def display_wireframe(self, screen):
        for edge in self.edges:
            pygame.draw.aaline(screen, self.wireframeColor,
                               topixel(edge.start.vx, edge.start.vy),
                               topixel(edge.end.vx, edge.end.vy))

    def display(self, screen):
        if self.wireframe:
            self.display_wireframe(screen)

    def setSurfaceForTransformed(self):
        for surface in self.surfaces:
            for vertex in surface.vertices:
                if vertex.transformed:
                    surface.setPlaneCoeffs()
                    surface.setCenter()
                    break
        for surface in self.surfaces:
            for vertex in surface.vertices:
                vertex.transformed = False

    def translate(self, x, y, z, camera):
        for vertex in self.vertices:
            vertex.x += x
            vertex.y += y
            vertex.z += z
        camera.setViewingValues(self.vertices)

    def translate_surfaces(self, surfaces, t, camera):
        a, b, c, d = surfaces[0].a, surfaces[0].b, surfaces[0].c, surfaces[0].d
        for surface in surfaces:
            if surface.a != a or surface.b != b or surface.c != c or surface.d != d:
                print("surfaces not lying in plane")
                return
        for surface in surfaces:
            for vertex in surface.vertices:
                if not vertex.transformed:
                    vertex.x += t[0]
                    vertex.y += t[1]
                    vertex.z += t[2]
                    vertex.transformed = True
                    camera.setViewingValues(vertex)
        self.setSurfaceForTransformed()

    def scale_surfaces(self, surfaces, scale, camera):
        #vertices = []
        a, b, c, d = surfaces[0].a, surfaces[0].b, surfaces[0].c, surfaces[0].d
        for surface in surfaces:
            if surface.a != a or surface.b != b or surface.c != c or surface.d != d:
                print("surfaces not lying in plane")
                return
        for surface in surfaces:
            for vertex in surface.vertices:
                if not vertex.transformed:
                    vertex.x *= scale[0]
                    vertex.y *= scale[1]
                    vertex.z *= scale[2]
                    vertex.transformed = True
                    camera.setViewingValues(vertex)
        self.setSurfaceForTransformed()

    def scale_surfaces_center(self, surfaces, scale, camera):
        center_x, center_y, center_z = 0, 0, 0
        for surface in surfaces:
            center_x += surface.center.x
            center_y += surface.center.y
            center_z += surface.center.z
        vn = len(surfaces)
        center_x /= vn  #centroid
        center_y /= vn
        center_z /= vn
        self.scale_surfacesFP(surfaces, scale, (center_x, center_y, center_z),
                              camera)

    def scale_surfacesFP(self, surfaces, scale, fp, camera):
        a, b, c, d = surfaces[0].a, surfaces[0].b, surfaces[0].c, surfaces[0].d
        for surface in surfaces:
            if surface.a != a or surface.b != b or surface.c != c or surface.d != d:
                print("surfaces not lying in plane")
                return
        for surface in surfaces:
            for vertex in surface.vertices:
                if not vertex.transformed:
                    tm1 = Transform_matrix.translate(-fp[0], -fp[1], -fp[2])
                    sm = Transform_matrix.scale(scale[0], scale[1], scale[2])
                    tm2 = Transform_matrix.translate(fp[0], fp[1], fp[2])
                    sm = tm2.dot(sm.dot(tm1))  #composite scaling matrix
                    camera.setViewingValues(vertex, sm)
                    vertex.transformed = True
        self.setSurfaceForTransformed()

    def extrude(self, surface, amount, axis, camera):
        '''creates new surfaces from existing surface by extruding the selected surface'''
        ext_x = 0
        ext_y = 0
        ext_z = 0
        ext = False
        if axis == 'n':
            #extrude normal to surface
            ext_x = amount * surface.a
            ext_y = amount * surface.b
            ext_z = amount * surface.c
            ext = True
        elif axis == 'x':
            ext_x = amount
            ext = True
        elif axis == 'y':
            ext_y = amount
            ext = True
        elif axis == 'z':
            ext_z = amount
            ext = True

        if ext:
            ext_surface = copy.deepcopy(surface)
            for vertex in ext_surface.vertices:
                vertex.x += ext_x
                vertex.y += ext_y
                vertex.z += ext_z
            camera.setViewingValues(ext_surface.vertices)
            ext_surface.setCenter()

            ##                v = numpy.array([[vertex.x],
            ##                                 [vertex.y],
            ##                                 [vertex.z],
            ##                                 [1       ]])
            ##                v = camera.W2Vm.dot(v)
            ##                vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
            ##                vertex.vx = vertex.vx * camera.Zvp / vertex.vz
            ##                vertex.vy = vertex.vy * camera.Zvp / vertex.vz

            i = 0
            n = len(surface.vertices) - 1
            while i < n:
                new_surface = Surface(surface.vertices[i],
                                      surface.vertices[i + 1],
                                      ext_surface.vertices[i + 1])
                new_surface.addVertex(ext_surface.vertices[i])
                self.addSurface(new_surface)
                i += 1
            new_surface = Surface(surface.vertices[n], surface.vertices[0],
                                  ext_surface.vertices[0])
            new_surface.addVertex(ext_surface.vertices[n])
            self.addSurface(new_surface)
            self.addSurface(ext_surface)
            self.surfaces.remove(surface)

    def inset(self, surface, amount, camera):
        '''creates new surfaces from existing surface by inseting the selected surface'''
        ##        center_x, center_y, center_z = 0.0, 0.0, 0.0
        ##        for vertex in surface.vertices:
        ##            center_x += vertex.x
        ##            center_y += vertex.y
        ##            center_z += vertex.z
        ##        vn = len(surface.vertices)
        ##        center_x /= vn    #centroid
        ##        center_y /= vn
        ##        center_z /= vn
        ext_surface = copy.deepcopy(surface)
        for vertex in ext_surface.vertices:
            ext_x = surface.center.x - vertex.x
            ext_y = surface.center.y - vertex.y
            ext_z = surface.center.z - vertex.z
            vertex.x += ext_x * amount
            vertex.y += ext_y * amount
            vertex.z += ext_z * amount
        camera.setViewingValues(ext_surface.vertices)
        ext_surface.setCenter()
        ##
        ##            v = numpy.array([[vertex.x],
        ##                             [vertex.y],
        ##                             [vertex.z],
        ##                             [1       ]])
        ##            v = camera.W2Vm.dot(v)
        ##            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
        ##            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
        ##            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

        i = 0
        n = len(surface.vertices) - 1
        while i < n:
            new_surface = Surface(surface.vertices[i], surface.vertices[i + 1],
                                  ext_surface.vertices[i + 1])
            new_surface.addVertex(ext_surface.vertices[i])
            self.addSurface(new_surface)
            i += 1
        new_surface = Surface(surface.vertices[n], surface.vertices[0],
                              ext_surface.vertices[0])
        new_surface.addVertex(ext_surface.vertices[n])
        self.addSurface(new_surface)
        self.addSurface(ext_surface)
        self.surfaces.remove(surface)


class Light:
    '''define point light source for intensity calculations'''
    def __init__(self,
                 pos,
                 intensity=1,
                 edgecolor=(255, 255, 255),
                 selected_color=(255, 255, 0)):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.i = intensity
        norm_abs = math.sqrt(self.x * self.x + self.y * self.y +
                             self.z * self.z)
        self.normvector = (self.x / norm_abs, self.y / norm_abs,
                           self.z / norm_abs)
        start = Vertex(self.x, self.y, self.z)
        end = Vertex(0, 0, 0)
        edge = Edge(start, end)
        self.vertices = [start, end]
        self.edges = [edge]
        self.edgecolor = edgecolor
        self.radius = 10
        self.rect = None
        self.selected = False
        self.selected_color = selected_color

    def display(self, screen):
        pygame.draw.aaline(
            screen, self.edgecolor,
            topixel(self.edges[0].start.vx, self.edges[0].start.vy),
            topixel(self.edges[0].end.vx, self.edges[0].end.vy))
        if self.selected:
            self.rect = pygame.draw.circle(
                screen, self.selected_color,
                topixel(self.edges[0].start.vx, self.edges[0].start.vy),
                self.radius)
        else:
            self.rect = pygame.draw.circle(
                screen, self.edgecolor,
                topixel(self.edges[0].start.vx, self.edges[0].start.vy),
                self.radius)

    def checkPoint(self):
        if self.rect:
            return self.rect.collidepoint(pygame.mouse.get_pos())

    def translate(self, tx, ty, tz, camera):
        self.vertices[0].x += tx
        self.vertices[0].y += ty
        self.vertices[0].z += tz
        camera.setViewingValues(self.vertices)
        self.x, self.y, self.z = self.vertices[0].x, self.vertices[
            0].y, self.vertices[0].z
        #print("light:", self.x, self.y, self.z)

    def rotate(self, angle, axis, camera):
        rm = Transform_matrix.rotate(angle, axis)
        camera.setViewingValues(self.vertices, rm)
        self.x, self.y, self.z = self.vertices[0].x, self.vertices[
            0].y, self.vertices[0].z
        #print("light:", self.x, self.y, self.z)
    def setIntensity(self, intensity=1):
        self.i = intensity


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
        s1 = Surface(v1, v4, v3)
        s1.addVertex(v2)
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
        cube.addSurface(s4)
        cube.addSurface(s5)

        self.models['cube'] = cube
        ## ------------------ ##

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

        start_x, end_x = Vertex(-span, 0, 0), Vertex(span, 0, 0)
        self.vertices.append(start_x)
        self.vertices.append(end_x)
        self.xaxis = Edge(start_x, end_x)

        start_z, end_z = Vertex(0, 0, -span), Vertex(0, 0, span)
        self.vertices.append(start_z)
        self.vertices.append(end_z)
        self.zaxis = Edge(start_z, end_z)

        curspan = gridspacing
        while curspan < span:
            start_edge1, end_edge1 = Vertex(-span, 0,
                                            curspan), Vertex(span, 0, curspan)
            self.vertices.append(start_edge1)
            self.vertices.append(end_edge1)
            edge1 = Edge(start_edge1, end_edge1)

            start_edge2, end_edge2 = Vertex(-span, 0, -curspan), Vertex(
                span, 0, -curspan)
            self.vertices.append(start_edge2)
            self.vertices.append(end_edge2)
            edge2 = Edge(start_edge2, end_edge2)

            start_edge3, end_edge3 = Vertex(curspan, 0,
                                            -span), Vertex(curspan, 0, span)
            self.vertices.append(start_edge3)
            self.vertices.append(end_edge3)
            edge3 = Edge(start_edge3, end_edge3)

            start_edge4, end_edge4 = Vertex(-curspan, 0,
                                            -span), Vertex(-curspan, 0, span)
            self.vertices.append(start_edge4)
            self.vertices.append(end_edge4)
            edge4 = Edge(start_edge4, end_edge4)

            self.edges.append(edge1)
            self.edges.append(edge2)
            self.edges.append(edge3)
            self.edges.append(edge4)
            curspan += gridspacing

    def display(self, screen):
        #drawing grid
        pygame.draw.aaline(screen, self.xaxis_color,
                           topixel(self.xaxis.start.vx, self.xaxis.start.vy),
                           topixel(self.xaxis.end.vx, self.xaxis.end.vy))
        pygame.draw.aaline(screen, self.zaxis_color,
                           topixel(self.zaxis.start.vx, self.zaxis.start.vy),
                           topixel(self.zaxis.end.vx, self.zaxis.end.vy))

        for edge in self.edges:
            pygame.draw.aaline(screen, self.grid_color,
                               topixel(edge.start.vx, edge.start.vy),
                               topixel(edge.end.vx, edge.end.vy))


class SurfaceSelection:
    def __init__(self,
                 selectable_color=(150, 150, 150),
                 selected_color=(200, 200, 200),
                 multiselect_color=(175, 175, 100)):
        self.selected_surface = None
        self.selected_surfaces = []
        self.selectable_surfaces = []
        self.selectable_color = selectable_color
        self.selected_color = selected_color
        self.multiselect_color = multiselect_color
        self.multiselect = False

    def display(self, screen):
        for surface in self.selectable_surfaces:
            surface_points = []
            for v in surface.vertices:
                surface_points.append(topixel(v.vx, v.vy))
            pygame.draw.polygon(screen, self.selectable_color, surface_points)
        if self.multiselect:
            for surface in self.selected_surfaces:
                surface_points = []
                for v in surface.vertices:
                    surface_points.append(topixel(v.vx, v.vy))
                pygame.draw.polygon(screen, self.multiselect_color,
                                    surface_points)
        if self.selected_surface:
            surface_points = []
            for v in self.selected_surface.vertices:
                surface_points.append(topixel(v.vx, v.vy))
            pygame.draw.polygon(screen, self.selected_color, surface_points)

##    def setSelectableSurfaces(self, model, mouse_point):
##        self.selectable_surfaces.clear()
##        for surface in model.surfaces:
##            if isInterior(mouse_point, surface.edges):
##                self.selectable_surfaces.append(surface)

    def setSelectedSurface(self, index):
        #index must be from self.selectable_surfaces
        if self.selectable_surfaces and index < len(
                self.selectable_surfaces) and index >= 0:
            self.selected_surface = self.selectable_surfaces[index]
        else:
            self.selected_surface = None

    def setSelectedSurfaces(self):
        #index must be from self.selectable_surfaces
        if self.selected_surface:
            self.selected_surfaces.append(self.selected_surface)
        else:
            self.selected_surface.clear()


##
##    def setSelectedSurfaces(self, index):
##        #index must be from self.selectable_surfaces
##        if self.selectable_surfaces and index < len(self.selectable_surfaces) and index >= 0:
##            self.selected_surfaces.append(self.selectable_surfaces[index])
##        else:
##            self.selected_surface.clear()
##
