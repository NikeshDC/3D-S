import numpy
import math


class Transform_matrix:
    @staticmethod
    def translate(tx:float, ty:float, tz:float):
        '''returns 4x4 matrix for 3D translation based on parameters specified'''
        return numpy.array([[1, 0, 0, tx],
                            [0, 1, 0, ty],
                            [0, 0, 1, tz],
                            [0, 0, 0,  1]])

    @staticmethod
    def scale(sx:float, sy:float, sz:float):
        '''returns 4x4 matrix for 3D translation based on parameters specified'''
        return numpy.array([[sx, 0,  0,  0],
                            [0,  sy, 0,  0],
                            [0,  0,  sz, 0],
                            [0,  0,  0,  1]])

    @staticmethod
    def rotate(angle: float, axis):
        '''returns 4x4 matrix for 3D translation based on angle(in degrees) and axis specified'''
        angle = angle/180*math.pi
        if axis == 'x':
            return numpy.array([[1, 0,                0,               0],
                                [0, math.cos(angle), -math.sin(angle), 0],
                                [0, math.sin(angle),  math.cos(angle), 0],
                                [0, 0,                0,               1]])
        elif axis == 'y':
            return numpy.array([[ math.cos(angle), 0,  math.sin(angle), 0],
                                [0,                1,  0,               0],
                                [-math.sin(angle), 0,  math.cos(angle), 0],
                                [0,                0,  0,               1]])
        elif axis == 'z':
            return numpy.array([[ math.cos(angle), math.sin(angle), 0, 0],
                                [-math.sin(angle), math.cos(angle), 0, 0],
                                [0,                0,               1, 0],
                                [0,                0,               0, 1]])

    @staticmethod
    def transform(vertex, tm):
        v = numpy.array([[vertex.x],
                         [vertex.y],
                         [vertex.z],
                         [1       ]])
        v = tm.dot(v)
        vertex.x, vertex.y, vertex.z = v [0][0], v[1][0], v[2][0]
    

class Camera:
    def constructUVN(self):
        #determine uvn vectors for viewing
        #n = vector(lookatpos to pos)
        self.n = numpy.array([-self.lookatpos[0]+self.x, -self.lookatpos[1]+self.y, -self.lookatpos[2]+self.z])
        self.n = self.n/numpy.linalg.norm(self.n)
        #u = normalize(cross ((0,1,0) and n)
        self.u = numpy.cross(numpy.array([0,1,0]),self.n)
        self.u = self.u/numpy.linalg.norm(self.u)
        #v = cross (n and u)
        self.v = numpy.cross(self.n, self.u)
        #rotation matrix = [u1 u2 u3 0;v1 v2 v3 0;n1 n2 n3 0;0 0 0 1]
        self.Rm = numpy.array([[self.u[0], self.u[1], self.u[2], 0],
                               [self.v[0], self.v[1], self.v[2], 0],
                               [self.n[0], self.n[1], self.n[2], 0],
                               [0,         0,         0,         1]])
        self.Tm = Transform_matrix.translate(-self.x, -self.y, -self.z)
        #world2viewing matrix = rotation matrix . translationmatrix(pos)
        self.W2Vm = self.Rm.dot(self.Tm)
        
    def __init__(self,pos, lookatpos, clippingPlanes, viewingPlane):
        '''construct camera at (pos.x,pos.y,pos.z) which specifies world-coordinate position for camera(viewing coordinate) origin & facing lookatpos
            with normal along the vector from lookatpos to pos'''
        self.x = pos[0] #pos.x
        self.y = pos[1] #pos.y
        self.z = pos[2] #pos.z
        self.lookatpos = (lookatpos[0], lookatpos[1], lookatpos[2])

        self.nearplane = clippingPlanes[0]
        self.farplane = clippingPlanes[1]
        #z-coordinate of viewing plane for perspective projection
        self.Zvp = viewingPlane                         #projection reference point is at origin of viewing coordinate
        self.models = []           #object of 'Model' or 'Grid' (having attributes 'Vertices' and 'dispaly')
        self.display_objects = []  #object having method 'dispaly'
        
        self.constructUVN()

    def lookat(self,lookatpos):
        '''change lookat position'''
        self.lookatpos = (lookatpos[0], lookatpos[1], lookatpos[2])
        self.constructUVN()

    def addModel(self, model):
        if model not in self.models:
            self.models.append(model)
            self.display_objects.append(model)

    def updateView(self):
        for model in self.models:
            self.setViewingValues(model.vertices)
        
    def setviewplane(self,viewplanez: float):
        self.Zvp = viewplanez

    def zoom(self, amount = 0.1):
        newZvp = self.Zvp + amount
        for model in self.models:
            for vertex in model.vertices:
                vertex.vx, vertex.vy = vertex.vx * newZvp / self.Zvp,  vertex.vy * newZvp / self.Zvp
        self.Zvp = newZvp

    def dispaly(self, screen):
        for model in self.display_objects:
            model.display(screen)

    def rotate(self, rx, ry):
        #rx is rotation angle about axis in zx plane and perpendicular to 'n'(z-axis)/parallel to uv plane of camera
        #ry is roatation angle about world-y axis
##        v = numpy.array([[self.x],
##                         [self.y],
##                         [self.z],
##                         [1     ]])
        z_axis_angle = math.degrees(math.atan(self.z/self.x))
        up_rot = Transform_matrix.rotate(-z_axis_angle,'y') .dot(Transform_matrix.rotate(ry,'z').dot(
                                            Transform_matrix.rotate(z_axis_angle,'y')))
        #v = Transform_matrix.rotate(rx,'y').dot(up_rot.dot(v))
        tm = Transform_matrix.rotate(rx,'y').dot(up_rot)
        Transform_matrix.transform(self, tm)
##        self.x, self.y, self.z = v[0][0], v[1][0], v[2][0]
        self.constructUVN()
        self.updateView()
        
        
    def translate(self, tx:float, ty:float, tz:float):
        self.x += tx
        self.y += ty
        self.z += tz
        self.constructUVN()
        self.updateView()

    def setViewingValues(self, vertices, tm = numpy.array([])):
        '''sets value of viewing coordinates of vertices list based on the camera W2Vmatrix using optional tranform matrix('tm') provided'''
        if not isinstance(vertices, list):  #if only a vertex is given, wrap it in list
            vertices = [vertices]
            
        if tm.size > 0:
            for vertex in vertices:
                v = numpy.array([[vertex.x],
                                 [vertex.y],
                                 [vertex.z],
                                 [1       ]])
                v = tm.dot(v)
                vertex.x, vertex.y, vertex.z = v [0][0], v[1][0], v[2][0]
                
                v = self.W2Vm.dot(v)    
                vertex.vx, vertex.vy, vertex.vz = v [0][0], v[1][0], v[2][0]
                vertex.vx = vertex.vx * self.Zvp / vertex.vz
                vertex.vy = vertex.vy * self.Zvp / vertex.vz
        else:
            for vertex in vertices:
                v = numpy.array([[vertex.x],
                                 [vertex.y],
                                 [vertex.z],
                                 [1       ]])
                v = self.W2Vm.dot(v)    
                vertex.vx, vertex.vy, vertex.vz = v [0][0], v[1][0], v[2][0]
                vertex.vx = vertex.vx * self.Zvp / vertex.vz
                vertex.vy = vertex.vy * self.Zvp / vertex.vz

        
