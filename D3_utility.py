import numpy
import math
from utility_2d import lineIntersects
from graphics_utility import Transform_matrix, Model, topixel, tonormal, topixelx, topixely
from settings import Window, Light, Shading
import time


class Camera:
    def constructUVN(self):
        #determine uvn vectors for viewing
        #n = vector(lookatpos to pos)
        self.n = numpy.array([
            -self.lookatpos[0] + self.x, -self.lookatpos[1] + self.y,
            -self.lookatpos[2] + self.z
        ])
        self.n = self.n / numpy.linalg.norm(self.n)
        #u = normalize(cross ((0,1,0) and n)
        self.u = numpy.cross(numpy.array([0, 1, 0]), self.n)
        self.u = self.u / numpy.linalg.norm(self.u)
        #v = cross (n and u)
        self.v = numpy.cross(self.n, self.u)
        #rotation matrix = [u1 u2 u3 0;v1 v2 v3 0;n1 n2 n3 0;0 0 0 1]
        self.Rm = numpy.array([[self.u[0], self.u[1], self.u[2], 0],
                               [self.v[0], self.v[1], self.v[2], 0],
                               [self.n[0], self.n[1], self.n[2], 0],
                               [0, 0, 0, 1]])
        self.Tm = Transform_matrix.translate(-self.x, -self.y, -self.z)
        #world2viewing matrix = rotation matrix . translationmatrix(pos)
        self.W2Vm = self.Rm.dot(self.Tm)

    def __init__(self, pos, lookatpos, clippingPlanes, viewingPlane):
        '''construct camera at (pos.x,pos.y,pos.z) which specifies world-coordinate position for camera(viewing coordinate) origin & facing lookatpos
            with normal along the vector from lookatpos to pos'''
        self.x = pos[0]  #pos.x
        self.y = pos[1]  #pos.y
        self.z = pos[2]  #pos.z
        self.lookatpos = (lookatpos[0], lookatpos[1], lookatpos[2])

        self.nearplane = clippingPlanes[0]
        self.farplane = clippingPlanes[1]
        #z-coordinate of viewing plane for perspective projection
        self.Zvp = viewingPlane  #projection reference point is at origin of viewing coordinate
        self.models = [
        ]  #object of 'Model' or 'Grid' (having attributes 'Vertices' and 'dispaly')
        self.display_objects = []  #object having method 'dispaly'
        self.lights = []

        self.constructUVN()

    def lookat(self, lookatpos):
        '''change lookat position'''
        self.lookatpos = (lookatpos[0], lookatpos[1], lookatpos[2])
        self.constructUVN()
        self.updateView()

    def addLight(self, light):
        if light not in self.lights:
            self.lights.append(light)
            self.models.append(light)
            self.display_objects.append(light)

    def addModel(self, model):
        if model not in self.models:
            self.models.append(model)
            self.display_objects.append(model)

    def addDisplayObject(self, dispobj):
        if dispobj not in self.display_objects:
            self.display_objects.append(dispobj)

    def updateView(self):
        for model in self.models:
            self.setViewingValues(model.vertices)
            for edge in model.edges:
                edge.setViewingSlope()

    def setviewplane(self, viewplanez: float):
        self.Zvp = viewplanez

    def zoom(self, amount=0.1):
        newZvp = self.Zvp + amount
        for model in self.models:
            for vertex in model.vertices:
                vertex.vx, vertex.vy = vertex.vx * newZvp / self.Zvp, vertex.vy * newZvp / self.Zvp
        self.Zvp = newZvp

    def display(self, screen):
        for model in self.display_objects:
            model.display(screen)

    def rotate(self, rx, ry):
        #rx is rotation angle about axis in zx plane and perpendicular to 'n'(z-axis)/parallel to uv plane of camera
        #ry is roatation angle about world-y axis
        ##        v = numpy.array([[self.x],
        ##                         [self.y],
        ##                         [self.z],
        ##                         [1     ]])
        z_axis_angle = math.degrees(math.atan(self.z / self.x))
        up_rot = Transform_matrix.rotate(-z_axis_angle, 'y').dot(
            Transform_matrix.rotate(ry, 'z').dot(
                Transform_matrix.rotate(z_axis_angle, 'y')))
        #v = Transform_matrix.rotate(rx,'y').dot(up_rot.dot(v))
        tm = Transform_matrix.rotate(rx, 'y').dot(up_rot)
        Transform_matrix.transform(self, tm)
        ##        self.x, self.y, self.z = v[0][0], v[1][0], v[2][0]
        self.constructUVN()
        self.updateView()

    def translate(self, tx: float, ty: float, tz: float):
        self.x += tx
        self.y += ty
        self.z += tz
        self.constructUVN()
        self.updateView()

    def setViewingValues(self, vertices, tm=numpy.array([])):
        '''sets value of viewing coordinates of vertices list based on the camera W2Vmatrix using optional tranform matrix('tm') provided'''
        if not isinstance(vertices,
                          list):  #if only a vertex is given, wrap it in list
            vertices = [vertices]

        if tm.size > 0:
            for vertex in vertices:
                v = numpy.array([[vertex.x], [vertex.y], [vertex.z], [1]])
                v = tm.dot(v)
                vertex.x, vertex.y, vertex.z = v[0][0], v[1][0], v[2][0]

                v = self.W2Vm.dot(v)
                vertex.vx, vertex.vy, vertex.vz = v[0][0], v[1][0], v[2][0]
                vertex.vx = vertex.vx * self.Zvp / vertex.vz
                vertex.vy = vertex.vy * self.Zvp / vertex.vz
        else:
            for vertex in vertices:
                v = numpy.array([[vertex.x], [vertex.y], [vertex.z], [1]])
                v = self.W2Vm.dot(v)
                vertex.vx, vertex.vy, vertex.vz = v[0][0], v[1][0], v[2][0]
                #print("(",vertex.vx,vertex.vy,vertex.vz,")", sep = ", ")
                vertex.vx = vertex.vx * self.Zvp / vertex.vz
                vertex.vy = vertex.vy * self.Zvp / vertex.vz
                #print("(",vertex.vx," , ",vertex.vy,")")

    def back_face_detection(self):
        look_vector = (self.lookatpos[0] - self.x, self.lookatpos[1] - self.y,
                       self.lookatpos[2] - self.z)
        for model in self.models:
            if isinstance(model, Model):
                for surface in model.surfaces:
                    look_dot_surface = surface.a * look_vector[
                        0] + surface.b * look_vector[
                            1] + surface.c * look_vector[2]
                    if look_dot_surface > 0:
                        surface.backface = True
                    else:
                        surface.backface = False

    def z_buffer_rendering(self,
                           screen,
                           window_min_x,
                           window_max_x,
                           window_min_y,
                           window_max_y,
                           onePixelInNormal,
                           scanline_min_x=-100,
                           scanline_max_x=100,
                           max_depth=-100):
        start_time = time.time()
        for model in self.models:
            if isinstance(model, Model):
                print("dsf", model.material.color)
        #initially set default depth to 1/max_depth and intesity to background intensity
        self.back_face_detection()
        init_z_inv = 1 / max_depth
        window_max_pix_x, window_max_pix_y = topixel(window_max_x,
                                                     window_max_y)
        window_min_pix_x, window_min_pix_y = topixel(window_min_x,
                                                     window_min_y)
        look_vector = (self.lookatpos[0] - self.x, self.lookatpos[1] - self.y,
                       self.lookatpos[2] - self.z)
        ##        window_del_x = window_max_pix_x - window_min_pix_x
        ##        window_del_y = window_max_pix_y - window_min_pix_y
        window_del_x = Window.width
        window_del_y = Window.height
        z_buffer = [init_z_inv for x in range(window_del_x * window_del_y)]
        z_time = time.time()
        #print(z_time - start_time)
        #print(len(z_buffer))
        for model in self.models:
            if isinstance(model, Model):
                #print(model.material.color)
                model.calcMinMaxViews()
                if model.shading == Shading.FLAT:
                    for surface in model.surfaces:  #flat shading
                        #print("surface: ", model.surfaces.index(surface))
                        if surface.backface:
                            #print("backface: ", model.surfaces.index(surface))
                            continue
                        c_vec = numpy.array((look_vector[0] + surface.a,
                                             look_vector[1] + surface.b,
                                             look_vector[2] + surface.c))
                        a = c_vec.dot(self.u)
                        b = c_vec.dot(self.v)
                        c = c_vec.dot(self.n)
                        svz = surface.vertices[0].vz
                        svx = surface.vertices[0].vx * svz / self.Zvp
                        svy = surface.vertices[0].vy * svz / self.Zvp
                        d = -(a * svx + b * svy + c * svz)
                        intensity = Light.ia * model.material.ka
                        for light in self.lights:

                            lvec = [
                                light.x - surface.center.x,
                                light.y - surface.center.y,
                                light.z - surface.center.z
                            ]
                            ldotn = (lvec[0] * surface.a +
                                     lvec[1] * surface.b + lvec[2] * surface.c)
                            norm_ldotn = math.sqrt(lvec[0] * lvec[0] +
                                                   lvec[1] * lvec[1] +
                                                   lvec[2] * lvec[2])
                            ldotn = ldotn / norm_ldotn
                            diff_intensity = max((ldotn * model.material.kd),
                                                 0)

                            vvec = [
                                self.x - surface.center.x,
                                self.y - surface.center.y,
                                self.z - surface.center.z
                            ]
                            h = (lvec[0] + vvec[0], lvec[1] + vvec[1],
                                 lvec[2] + vvec[2])
                            hdotn = (h[0] * surface.a + h[1] * surface.b +
                                     h[2] * surface.c)
                            norm_hdotn = math.sqrt(h[0] * h[0] + h[1] * h[1] +
                                                   h[2] * h[2])
                            hdotn = hdotn / norm_hdotn
                            spec_intensity = max(
                                model.material.ks * (hdotn**model.material.ns),
                                0)

                            dist = lvec[0] * lvec[0] + lvec[1] * lvec[
                                1] + lvec[2] * lvec[2]

                            intensity += light.i * (
                                diff_intensity +
                                spec_intensity) / (Light.a0 + Light.a2 * dist)
                        # print(model.material.color)
                        # print(model.material.ka)
                        # print(model.material.kd)
                        _color = (int(
                            min(model.material.color[0] * intensity,
                                Light.mpv)),
                                  int(
                                      min(model.material.color[1] * intensity,
                                          Light.mpv)),
                                  int(
                                      min(model.material.color[2] * intensity,
                                          Light.mpv)))  #flatshading
                        #print(_color)

                        cur_y = min(surface.max_vy, window_max_y)
                        cur_pix_y = topixely(cur_y)
                        while cur_y >= max(surface.min_vy, window_min_y):
                            scanline = ((scanline_min_x, cur_y),
                                        (scanline_max_x, cur_y))
                            #intersected_edges = []
                            intersected_points = []
                            for edge in surface.edges:
                                _edge = ((edge.start.vx, edge.start.vy),
                                         (edge.end.vx, edge.end.vy))
                                if (lineIntersects(_edge, scanline)):
                                    #intersected_edges.append(edge)
                                    intersect_x = (cur_y - edge.end.vy
                                                   ) * edge.m_inv + edge.end.vx
                                    intersected_points.append(intersect_x)
                            #sorting the edges based on xvalues of intersected points
                            #intersected_points.sort(key = lambda point: point[0])
                            intersected_points.sort()
                            if len(intersected_points) % 2 != 0:
                                print(
                                    "Before: Odd number of intersections in z-buffer"
                                )
                                print(intersected_points)
                                print(model.surfaces.index(surface))
                                return

                            min_index = 0
                            max_index = 0  #position from last
                            n = len(intersected_points) - 1
                            min_x = intersected_points[0]
                            max_x = intersected_points[-1]
                            #print("intersects: ",intersected_points)
                            #finding minimum x-position to start drawing from
                            while min_x < window_min_x:
                                min_index += 1
                                if min_index >= len(intersected_points):
                                    break
                                min_x = intersected_points[min_index]
                            #finding maximum x-position to stop drawing at
                            while max_x > window_max_x:
                                max_index += 1
                                if n - max_index < 0:
                                    break
                                max_x = intersected_points[n - max_index]

                            if min_index > (n - max_index):
                                intersected_points = [
                                    window_min_x, window_max_x
                                ]
                            else:
                                if min_index > 0:
                                    del intersected_points[0:min_index]
                                new_n = len(intersected_points) - 1
                                if (new_n - max_index + 1) <= new_n:
                                    del intersected_points[new_n - max_index +
                                                           1:new_n + 1]

                                #if minimun index is even then it is starting edge of surface and if odd it is ending edge
                                if min_index % 2 == 1:
                                    intersected_points.insert(0, window_min_x)
                                #if maximun index is even then it is ending edge of surface and if odd it is satrting edge
                                if max_index % 2 == 1:
                                    intersected_points.append(window_max_x)

                            if len(intersected_points) % 2 != 0:
                                print(
                                    "After: Odd number of intersections in z-buffer"
                                )
                                print(intersected_points)
                                print(model.surfaces.index(surface))
                                return

                            #z-value computation starts now
                            i = 0
                            k = -a * onePixelInNormal / (d * self.Zvp)
                            while i < (len(intersected_points) - 1):
                                #initial 1/z value
                                z_inv = (a * intersected_points[i] + b * cur_y
                                         + c * self.Zvp) / (-d * self.Zvp)
                                cur_x = intersected_points[i]
                                next_x = intersected_points[i + 1]
                                next_pix_x = topixelx(next_x)
                                cur_pix_x = topixelx(cur_x)
                                while cur_pix_x <= next_pix_x:
                                    z_index = cur_pix_x * window_del_y + cur_pix_y
                                    #print(z_index)
                                    try:
                                        if z_inv < z_buffer[z_index]:
                                            z_buffer[z_index] = z_inv
                                            screen.set_at(
                                                (cur_pix_x, cur_pix_y), _color)
                                    except Exception as e:
                                        print(cur_pix_x, cur_pix_y)
                                    z_inv += k
                                    cur_pix_x += 1
                                    cur_x += onePixelInNormal
                                i += 2
                            cur_pix_y += 1
                            cur_y -= onePixelInNormal

                elif model.shading == Shading.GOURAUD:
                    model.setVertexNormals()
                    for vertex in model.vertices:  #setting vertex intensities
                        vertex.intensity = Light.ia * model.material.kd
                        for light in self.lights:
                            lvec = [
                                light.x - vertex.x, light.y - vertex.y,
                                light.z - vertex.z
                            ]
                            ldotn = (lvec[0] * vertex.normal[0] +
                                     lvec[1] * vertex.normal[1] +
                                     lvec[2] * vertex.normal[2])
                            norm_ldotn = math.sqrt(lvec[0] * lvec[0] +
                                                   lvec[1] * lvec[1] +
                                                   lvec[2] * lvec[2])
                            ldotn = ldotn / norm_ldotn
                            diff_intensity = max((ldotn * model.material.kd),
                                                 0)

                            vvec = [
                                self.x - vertex.x, self.y - vertex.y,
                                self.z - vertex.z
                            ]
                            h = (lvec[0] + vvec[0], lvec[1] + vvec[1],
                                 lvec[2] + vvec[2])
                            hdotn = (h[0] * vertex.normal[0] +
                                     h[1] * vertex.normal[1] +
                                     h[2] * vertex.normal[2])
                            norm_hdotn = math.sqrt(h[0] * h[0] + h[1] * h[1] +
                                                   h[2] * h[2])
                            hdotn = hdotn / norm_hdotn
                            spec_intensity = max(
                                model.material.ks * (hdotn**model.material.ns),
                                0)

                            dist = lvec[0] * lvec[0] + lvec[1] * lvec[
                                1] + lvec[2] * lvec[2]

                            vertex.intensity += light.i * (
                                diff_intensity +
                                spec_intensity) / (Light.a0 + Light.a2 * dist)

                    for surface in model.surfaces:  #gouraud shading
                        if surface.backface:
                            continue
                        c_vec = numpy.array((look_vector[0] + surface.a,
                                             look_vector[1] + surface.b,
                                             look_vector[2] + surface.c))
                        a = c_vec.dot(
                            self.u
                        )  #calculating a,b,c,d in terms of viewing coordinate
                        b = c_vec.dot(self.v)
                        c = c_vec.dot(self.n)
                        svz = surface.vertices[0].vz
                        svx = surface.vertices[0].vx * svz / self.Zvp
                        svy = surface.vertices[0].vy * svz / self.Zvp
                        d = -(a * svx + b * svy + c * svz)

                        cur_y = min(surface.max_vy, window_max_y)
                        cur_pix_y = topixely(cur_y)
                        while cur_y >= max(surface.min_vy, window_min_y):
                            scanline = ((scanline_min_x, cur_y),
                                        (scanline_max_x, cur_y))
                            intersected_points = []
                            for edge in surface.edges:
                                _edge = ((edge.start.vx, edge.start.vy),
                                         (edge.end.vx, edge.end.vy))
                                if (lineIntersects(_edge, scanline)):
                                    intersect_x = (cur_y - edge.end.vy
                                                   ) * edge.m_inv + edge.end.vx
                                    intersected_points.append(
                                        (intersect_x, edge))
                            intersected_points.sort(key=lambda point: point[0])
                            if len(intersected_points) % 2 != 0:
                                print(
                                    "Before: Odd number of intersections in z-buffer"
                                )
                                print(intersected_points)
                                print(model.surfaces.index(surface))
                                return

                            min_index = 0
                            max_index = 0  #position from last
                            n = len(intersected_points) - 1
                            min_x = intersected_points[0][0]
                            max_x = intersected_points[-1][0]
                            #print("intersects: ",intersected_points)
                            #finding minimum x-position to start drawing from
                            while min_x < window_min_x:
                                min_index += 1
                                min_x = intersected_points[min_index][0]
                            #finding maximum x-position to stop drawing at
                            while max_x > window_max_x:
                                max_index += 1
                                max_x = intersected_points[n - max_index][0]

                            if min_index > (n - max_index):
                                intersected_points = [
                                    window_min_x, window_max_x
                                ]
                            else:
                                if min_index > 0:
                                    del intersected_points[0:min_index]
                                new_n = len(intersected_points) - 1
                                if (new_n - max_index + 1) <= new_n:
                                    del intersected_points[new_n - max_index +
                                                           1:new_n + 1]

                                #if minimun index is even then it is starting edge of surface and if odd it is ending edge
                                if min_index % 2 == 1:
                                    intersected_points.insert(0, window_min_x)
                                #if maximun index is even then it is ending edge of surface and if odd it is satrting edge
                                if max_index % 2 == 1:
                                    intersected_points.append(window_max_x)

                            if len(intersected_points) % 2 != 0:
                                print(
                                    "After: Odd number of intersections in z-buffer"
                                )
                                print(intersected_points)
                                print(model.surfaces.index(surface))
                                return

                            #z-value computation starts now
                            i = 0
                            k = -a * onePixelInNormal / (d * self.Zvp)
                            while i < (len(intersected_points) - 1):
                                cur_x = intersected_points[i][0]
                                next_x = intersected_points[i + 1][0]
                                next_pix_x = topixelx(next_x)
                                cur_pix_x = topixelx(cur_x)
                                #initial 1/z value
                                z_inv = (a * cur_x + b * cur_y +
                                         c * self.Zvp) / (-d * self.Zvp)
                                i1 = intersected_points[i][1].start.intensity
                                y1 = intersected_points[i][1].start.vy
                                i2 = intersected_points[i][1].end.intensity
                                y2 = intersected_points[i][1].end.vy
                                i3 = intersected_points[i +
                                                        1][1].start.intensity
                                y3 = intersected_points[i + 1][1].start.vy
                                i4 = intersected_points[i + 1][1].end.intensity
                                y4 = intersected_points[i + 1][1].end.vy
                                i5 = (cur_y - y2) * i1 / (y1 - y2) + (
                                    y1 - cur_y) * i2 / (y1 - y2)
                                i6 = (cur_y - y4) * i3 / (y3 - y4) + (
                                    y3 - cur_y) * i4 / (y3 - y4)
                                if cur_x != next_x:
                                    ik = (i6 - i5) * onePixelInNormal / (
                                        next_x - cur_x)
                                else:
                                    ik = 0.0
                                _intensity = i5
                                while cur_pix_x <= next_pix_x:
                                    z_index = cur_pix_x * window_del_y + cur_pix_y
                                    #print(z_index)
                                    if z_inv < z_buffer[z_index]:
                                        z_buffer[z_index] = z_inv
                                        _color = (
                                            int(
                                                min(
                                                    model.material.color[0] *
                                                    _intensity, Light.mpv)),
                                            int(
                                                min(
                                                    model.material.color[1] *
                                                    _intensity, Light.mpv)),
                                            int(
                                                min(
                                                    model.material.color[2] *
                                                    _intensity, Light.mpv)))
                                        screen.set_at((cur_pix_x, cur_pix_y),
                                                      _color)
                                    _intensity += ik
                                    z_inv += k
                                    cur_pix_x += 1
                                    cur_x += onePixelInNormal
                                i += 2
                            cur_pix_y += 1
                            cur_y -= onePixelInNormal

        end_time = time.time()
        #print(end_time - start_time)


##    def z_buffer_rendering(self, window_min_x, window_max_x,onePixelInNormal, scanline_min_x = -100, scanline_max_x = 100,):
##        for model in self.models:
##            #if isinstance(model, Model):
##                for surface in model.surfaces:
##                    if surface.backface:
##                        continue
##
##                    cur_y = surface.vertices[0].vy
##                    for vertex in surface.vertices:
##                        if vertex.vy < cur_y:
##                            #minimun viewing y coordinate
##                            cur_y = vertex.vy
##                    scanline = ((scanline_min_x, cur_y),(scanline_max_x, cur_y))
##                    intersected_edges = []
##                    intersected_points = []
##                    for edge in surface.edges:
##                        _edge = ((edge.start.vx, edge.start.vy),(edge.end.vx, edge.end.vy))
##                        if (lineIntersects(_edge, scanline)):
##                            #intersected_edges.append(edge)
##                            intersect_x = (cur_y - edge.start.vy) * edge.m_inv + edge.start.vx
##                            intersected_points.append((intersect_x, edge))
##                    #sorting the edges based on xvalues of intersected points
##                    intersected_points.sort(key = lambda point: point[0])
##
##                    min_index = 0
##                    max_index = len(intersected_points) - 1
##                    min_x = intersected_points[0][0]
##                    max_x = intersected_points[-1][0]
##                    #finding minimum x-position to start drawing from
##                    while min_x < window_min_x:
##                        min_index += 1
##                        min_x = intersected_points[min_index][0]
##                    #finding maximum x-position to stop drawing at
##                    while max_x > window_min_x:
##                        max_index -= 1
##                        max_x = intersected_points[max_index][0]
##
##                    #if minimun index is even then it is starting edge of surface and if odd it is ending edge
##                    if min_index % 2 == 1:
##                        intersected_points.insert(0, window_min_x)
##                    if max_index % 2 == 0:
##                        intersected_points.append(window_max_x)
##
##
##
##
##                        #form pair
##                    if len(intersected_points) % 2 != 0:
##                        print("Odd number of intersections in z-buffer")
##                        return
