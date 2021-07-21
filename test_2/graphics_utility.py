import math
from D3_utility import *
import copy

class Vertex:
    '''class for representing vertex in a 3D-coordinate'''
    def __init__(self,x: float,y: float,z: float):
        self.x = x     #coordinate values of vertex in world view
        self.y = y
        self.z = z
        
        #coordinate values of vertices for viewing co-ordinate/ or perspective viewing
        self.vx = x     
        self.vy = y
        self.vz = z

    def __eq__(self,v):
        return ((self.x == v.x) and (self.y == v.y) and (self.z == v.z))
    def __ne__(self,v):
        return (self.x != v.x or self.y != v.y or self.z != v.z)
        

class Edge:
    '''class for representing edge in a 3D-coordinate'''
    def __init__(self,v1: Vertex,v2: Vertex):
        self.start = v1
        self.end = v2


class Surface:
    '''class for representing surface in a 3D-coordinate'''
    @staticmethod
    def getPlaneCoeffs(v1: Vertex, v2: Vertex, v3: Vertex):
        '''returns the coefficient A,B,C&D of the plane  Ax+By+Cz+D=0 represented by the vertices provided'''
        #(a,b,c) = (v2 - v1)cross(v3 - v1); d = -(a*v1.x + b*v1.y +c*v1.z)
        a = -(v1.y*(v2.z - v3.z) + v2.y*(v3.z - v1.z) + v3.y*(v1.z - v2.z))
        b = -(v1.z*(v2.x - v3.x) + v2.z*(v3.x - v1.x) + v3.z*(v1.x - v2.x))
        c = -(v1.x*(v2.y - v3.y) + v2.x*(v3.y - v1.y) + v3.x*(v1.y - v2.y))
        d = -(-v1.x*(v2.y*v3.z - v3.y*v2.z) - v2.x*(v3.y*v1.z - v1.y*v3.z) - v3.x*(v1.y*v2.z - v2.y*v1.z))
        norm_abs = math.sqrt(a*a + b*b + c*c)
        a,b,c,d = a/norm_abs, b/norm_abs, c/norm_abs, d/norm_abs #normalizing to get normal vectors
        #print("a:",a," b:",b," c:",c," d:",d)
        return (a,b,c,d)
    
    def setPlaneCoeffs(self):
        self.a,self.b,self.c,self.d = Surface.getPlaneCoeffs(self.vertices[0],self.vertices[1],self.vertices[2])
        
    def __init__(self,v1: Vertex,v2: Vertex,v3: Vertex):
        '''makes surface from 3 vertices specified in conterclockwise direction with respect to required normal'''
        e1 = Edge(v1,v2)
        e2 = Edge(v2,v3)
        e3 = Edge(v3,v1)
        self.edges = [e1,e2,e3]
        self.a,self.b,self.c,self.d = Surface.getPlaneCoeffs(v1,v2,v3)
        self.vertices = [v1,v2,v3]

    def addVertex(self,v):
        #v = projection of v on plane made by first three vertices
        a,b,c,d = self.a, self.b, self.c, self.d
        #t = -(a*v.x + b*v.y + c*v.z + d)/math.sqrt(a*a + b*b + c*c) ;already normalized (math.sqrt(a*a + b*b + c*c) = 1)
        t = -(a*v.x + b*v.y + c*v.z + d)
        newv = Vertex(0,0,0)
        newv.x, newv.y, newv.z = a*t + v.x, b*t + v.y, c*t + v.z
        if not(newv == v):
            print(f"vertex not lying in plane vertex:({v.x},{v.y},{v.z})  \nprojection:({newv.x},{newv.y},{newv.z})")
            return
        if v in self.vertices:
            print("vertex already included in surface")
            return
        
        vend = self.edges[-1].end
        vstart = self.edges[-1].start
        self.edges.pop()  #removing last edge to make new edges connecting to the new vertex
        self.edges.append(Edge(vstart, v))
        self.edges.append(Edge(v, vend))
        self.vertices.append(v)

    def translate(self, tx,ty,tz, camera):
        for vertex in self.vertices:
            vertex.x += tx
            vertex.y += ty
            vertex.z += tz

            v = numpy.array([[vertex.x],
                             [vertex.y],
                             [vertex.z],
                             [1       ]])
            v = camera.W2Vm.dot(v)
            
            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def rotate(self, angle, axis, camera):
        '''rotate about given axis('x' / 'y' / 'z') with world origin as fixed point'''
        rm = Transform_matrx.rotate(angle, axis)
        for vertex in self.vertices:
            v = numpy.array([[vertex.x],
                             [vertex.y],
                             [vertex.z],
                             [1       ]])
            v = rm.dot(v)
            vertex.x, vertex.y, vertex.z = v [0], v[1], v[2]
            
            v = camera.W2Vm.dot(v)
            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def rotate_center(self, angle, axis, camera):
        '''rotate about given axis('x' / 'y' / 'z') with center of the surface as fixed point'''
        center_x, center_y, center_z = 0.0, 0.0, 0.0
        for vertex in self.vertices:
            center_x += vertex.x
            center_y += vertex.y
            center_z += vertex.z
        vn = len(self.vertices)
        center_x /= vn     #centroid
        center_y /= vn
        center_z /= vn
        self.rotateFP(center_x, center_y, center_z, angle, axis, camera)

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
        rm = tm2.dot(rm.dot(tm1))    #composite rotation matrix
        for vertex in self.vertices:
            v = numpy.array([[vertex.x],
                             [vertex.y],
                             [vertex.z],
                             [1       ]])
            v = rm.dot(v)
            vertex.x, vertex.y, vertex.z = v [0], v[1], v[2]
            
            v = camera.W2Vm.dot(v)
            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def scale(self, sx,sy,sz, camera):
        for vertex in self.vertices:
            vertex.x *= sx
            vertex.y *= sy
            vertex.z *= sz

            v = numpy.array([[vertex.x],
                             [vertex.y],
                             [vertex.z],
                             [1       ]])
            v = camera.W2Vm.dot(v)
            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
            vertex.vy = vertex.vy * camera.Zvp / vertex.vz

    def scale_center(self, sx,sy,sz, camera):
        '''scale about center of the surface as fixed point'''
        center_x, center_y, center_z = 0.0, 0.0, 0.0    
        for vertex in self.vertices:
            center_x += vertex.x
            center_y += vertex.y
            center_z += vertex.z
        vn = len(self.vertices)
        center_x /= vn    #centroid
        center_y /= vn
        center_z /= vn
        self.scaleFP(center_x, center_y, center_z, sx, sy, sz, camera)

        
    def scaleFP(self, fx, fy, fz, sx, sy, sz, camera):
        '''rotate the surface about fixed point about given axis('x' / 'y' / 'z') about fixed point'''
        tm1 = Transform_matrix.translate(-fx, -fy, -fz)
        sm = Transform_matrix.scale(sx, sy, sz)
        tm2 = Transform_matrix.translate(fx, fy, fz)
        sm = tm2.dot(sm.dot(tm1))   #composite scaling matrix
        for vertex in self.vertices:
            v = numpy.array([[vertex.x],
                             [vertex.y],
                             [vertex.z],
                             [1       ]])
            v = sm.dot(v)
            vertex.x, vertex.y, vertex.z = v [0], v[1], v[2]
            
            v = camera.W2Vm.dot(v)    
            vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
            vertex.vx = vertex.vx * camera.Zvp / vertex.vz
            vertex.vy = vertex.vy * camera.Zvp / vertex.vz
            
        



class Model:
    '''class for representing a object in a 3D-coordinate'''
    def __init__(self):
        self.surfaces = []
        self.vertices = []
        self.edges = []

    def addSurface(self,s: Surface):
        self.surfaces.append(s)
        for vertex in s.vertices:
            if not vertex in self.vertices:
                self.vertices.append(vertex)
        for edge in s.edges:
            if not edge in self.edges:
                self.edges.append(edge)

    def setViewPlaneCoeffs(self):
        for surface in self.surfaces:
            surface.setViewPlaneCoeffs()

    def translate(self,x,y,z):
        for vertex in self.vertices:
            vertex.x += x
            vertex.y += y
            vertex.z += z

    def extrude(self, surface, amount, axis, camera):
        '''creates new surfaces from existing surface by extruding the selected surface'''
        if axis == 'n':
            #extrude normal to surface
            ext_surface = copy.deepcopy(surface)
            for vertex in ext_surface.vertices:
                vertex.x += amount * surface.a
                vertex.y += amount * surface.b
                vertex.z += amount * surface.c

                v = numpy.array([[vertex.x],
                                 [vertex.y],
                                 [vertex.z],
                                 [1       ]])
                v = camera.W2Vm.dot(v)    
                vertex.vx, vertex.vy, vertex.vz = v [0], v[1], v[2]
                vertex.vx = vertex.vx * camera.Zvp / vertex.vz
                vertex.vy = vertex.vy * camera.Zvp / vertex.vz
                
            i = 0
            n = len(surface.vertices) - 1
            while i < n:
                new_surface = Surface(surface.vertices[i],surface.vertices[i+1],ext_surface.vertices[i+1])
                new_surface.addVertex(ext_surface.vertices[i])
                self.addSurface(new_surface)
                i += 1
            new_surface = Surface(surface.vertices[n],surface.vertices[0],ext_surface.vertices[0])
            new_surface.addVertex(ext_surface.vertices[n])
            self.addSurface(new_surface)
            self.addSurface(ext_surface)
            self.surfaces.remove(surface)


class StandardModels:
    def __init__(self):
        '''class to contain the standard in-built models avialable for 3d-modeling'''
        self.models = {}

        ## ------ cube ------ ##
        cube = Model()
        v1 = Vertex(0.0,0.0,0.0)
        v2 = Vertex(2.0,0.0,0.0)
        v3 = Vertex(2.0,1.0,0.0)
        v4 = Vertex(0.0,1.0,0.0)
        v5 = Vertex(0.0,1.0,1.0)
        v6 = Vertex(0.0,0.0,1.0)
        v7 = Vertex(2.0,0.0,1.0)
        v8 = Vertex(2.0,1.0,1.0)
        s1 = Surface(v1,v2,v3)
        s1.addVertex(v4)
        s2 = Surface(v1,v4,v5)
        s2.addVertex(v6)
        s3 = Surface(v5,v8,v7)
        s3.addVertex(v6)
        s4 = Surface(v8,v3,v2)
        s4.addVertex(v7)
        s5 = Surface(v4,v3,v8)
        s5.addVertex(v5)
        s6 = Surface(v1,v6,v7)
        s6.addVertex(v2)
        cube.addSurface(s2)
        cube.addSurface(s1)
        cube.addSurface(s6)
        cube.addSurface(s3)
        cube.addSurface(s4)
        cube.addSurface(s5)

        self.models['cube'] = cube
        ## ------------------ ##

        
class Grid:
    '''class to create a grid spanning on xz-plane'''
    def __init__(self, gridspacing, span, grid_color, xaxis_color, zaxis_color):
        self.edges = []
        self.vertices = []
        self.grid_color = grid_color
        self.xaxis_color = xaxis_color
        self.zaxis_color = zaxis_color
        
        
        self.xaxis = Edge(Vertex(-span,0,0), Vertex(span,0,0))
        self.zaxis = Edge(Vertex(0,0,-span), Vertex(0,0,span))
        curspan = gridspacing
        while curspan < span:
            edge1 = Edge(Vertex(-span,0,curspan), Vertex(span,0,curspan))
            edge2 = Edge(Vertex(-span,0,-curspan), Vertex(span,0,-curspan))
            edge3 = Edge(Vertex(curspan,0,-span), Vertex(curspan,0,span))
            edge4 = Edge(Vertex(-curspan,0,-span), Vertex(-curspan,0,span))
            self.edges.append(edge1)
            self.edges.append(edge2)
            self.edges.append(edge3)
            self.edges.append(edge4)
            curspan += gridspacing
        
