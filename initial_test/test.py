import pygame
from pygame import gfxdraw
import sys
from graphics_utility import *
from D3_utility import *
from utility_2d import *
import numpy


#print(lineIntersects(((7,7),(5,5)),((5,0),(0,5))))

##abc = True
##xyz = True

screen_x = 1280
screen_y = 720

#account for different dimensions of screen width and height to draw proportionately
screen_xy = min(screen_x,screen_y)

def topixel(x,y):
    '''converts normalized value to actual pixel values'''
    x = int((screen_x + x*screen_xy)/2)
    y = int((screen_y - y*screen_xy)/2)
    return (x,y)

def tonormal(x,y):
    '''converts pixel value to normalized value'''
    x = float((2*x - screen_x)/screen_xy)
    y = float((-2*y + screen_y)/screen_xy)
    return (x,y)

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("3Ds")
bgcolor = (99,99,99)
line_color = (241,165,5)
gridcolor = (120, 120, 120)
xaxiscolor = (28, 217, 44)
zaxiscolor = (237, 15, 2)
surfacecolor = (170,170,170)
selected_color = (220,220,220)

grid = Grid(1.0,10.0,gridcolor, xaxiscolor, zaxiscolor)
m1 = StandardModels().models['cube']

campos = (15.0,15.0,10.0)
lookatpos = [0.0,0.0,0.0]
clippingplanes = (5.0,25.0)
viewplane = 5.0
mainCamera = Camera(campos,lookatpos, clippingplanes, viewplane)

#transforming model to viewing coordinates -------------------------------
for vertex in m1.vertices:
    v = numpy.array([[vertex.x],
                     [vertex.y],
                     [vertex.z],
                     [1       ]])
    v = mainCamera.W2Vm.dot(v)
    # perspective viewing
    vertex.x = v[0] / v[2] * mainCamera.Zvp
    vertex.y = v[1] / v[2] * mainCamera.Zvp
#-----------------------------------------transforming model to viewing coordinates
    

#transforming grid ------------------------------------------------------
for edge in grid.edges:
    v = numpy.array([[edge.start.x, edge.end.x],
                     [edge.start.y, edge.end.y],
                     [edge.start.z, edge.end.z],
                     [1,            1         ]])
    v = mainCamera.W2Vm.dot(v)
    # perspective viewing
    edge.start.x = v[0][0] / v[2][0] * mainCamera.Zvp
    edge.start.y = v[1][0] / v[2][0] * mainCamera.Zvp
    edge.end.x   = v[0][1] / v[2][1] * mainCamera.Zvp
    edge.end.y   = v[1][1] / v[2][1] * mainCamera.Zvp

#for the x and z axis
v = numpy.array([[grid.xaxis.start.x, grid.xaxis.end.x, grid.zaxis.start.x, grid.zaxis.end.x],
                 [grid.xaxis.start.y, grid.xaxis.end.y, grid.zaxis.start.y, grid.zaxis.end.y],
                 [grid.xaxis.start.z, grid.xaxis.end.z, grid.zaxis.start.z, grid.zaxis.end.z],
                 [1,                  1,                1,                  1               ]])
v = mainCamera.W2Vm.dot(v)
grid.xaxis.start.x = v[0][0] / v[2][0] * mainCamera.Zvp
grid.xaxis.start.y = v[1][0] / v[2][0] * mainCamera.Zvp
grid.xaxis.end.x   = v[0][1] / v[2][1] * mainCamera.Zvp
grid.xaxis.end.y   = v[1][1] / v[2][1] * mainCamera.Zvp
grid.zaxis.start.x = v[0][2] / v[2][2] * mainCamera.Zvp
grid.zaxis.start.y = v[1][2] / v[2][2] * mainCamera.Zvp
grid.zaxis.end.x   = v[0][3] / v[2][3] * mainCamera.Zvp
grid.zaxis.end.y   = v[1][3] / v[2][3] * mainCamera.Zvp
#-------------------------------------------------------------transforming grid

_surfacecolor = surfacecolor

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            abc = True
            xyz = True
        mousex, mousey = pygame.mouse.get_pos()
        mousex, mousey = tonormal(mousex, mousey)
        mouse_point = Vertex(mousex,mousey,0)

##        si = 0
##        for surface in m1.surfaces:
##            if checkForPointInside(mouse_point, surface.edges):
##                print("Inside",si)
##            si += 1
            
        
        screen.fill(bgcolor)

        #drawing grid
        pygame.draw.aaline(screen, grid.xaxis_color, topixel(grid.xaxis.start.x, grid.xaxis.start.y), topixel(grid.xaxis.end.x, grid.xaxis.end.y))
        pygame.draw.aaline(screen, grid.zaxis_color, topixel(grid.zaxis.start.x, grid.zaxis.start.y), topixel(grid.zaxis.end.x, grid.zaxis.end.y))
##        gz_xs,gz_ys = topixel(grid.zaxis.start.x, grid.zaxis.start.y)
##        gz_xe,gz_ye = topixel(grid.zaxis.end.x, grid.zaxis.end.y)
##        pygame.gfxdraw.line(screen, gz_xs, gz_ys, gz_xe, gz_ye, grid.zaxis_color)
        for edge in grid.edges:
            #pygame.draw.line(screen, grid.grid_color, topixel(edge.start.x, edge.start.y), topixel(edge.end.x, edge.end.y),1)
            pygame.draw.aaline(screen, grid.grid_color, topixel(edge.start.x, edge.start.y), topixel(edge.end.x, edge.end.y))

        #drawing cube-model ->surface
        for surface in m1.surfaces:
            if isInterior(mouse_point, surface.edges):
                _surfacecolor = selected_color
            else:
                _surfacecolor = surfacecolor
            surface_points = []
            for v in surface.vertices:
                surface_points.append(topixel(v.x,v.y))
            pygame.draw.polygon(screen, _surfacecolor, surface_points)
        #drawing cube-model ->edges
        for surface in m1.surfaces:
            for edge in surface.edges:
                pygame.draw.aaline(screen, line_color, topixel(edge.start.x, edge.start.y), topixel(edge.end.x, edge.end.y))

        
                

    pygame.display.flip()
