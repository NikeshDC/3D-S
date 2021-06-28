import pygame
import sys
from graphics_utility import *
from D3_utility import *
import numpy 

screen_x = 600
screen_y = 600

def topixel(x,y):
    '''converts normalized value to actual pixel values'''
    x = int((screen_x - x*screen_x)/2)
    y = int((screen_y - y*screen_y)/2)
    return (x,y)

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("3Ds")
bgcolor = (99,99,99)
line_color = (241,165,5)
gridcolor = (212, 212, 212)
xaxiscolor = (28, 217, 44)
zaxiscolor = (237, 15, 2)

grid = Grid(1.0,10.0,gridcolor, xaxiscolor, zaxiscolor)
m1 = StandardModels().models['cube']

campos = (15.0,15.0,10.0)
lookatpos = [0.0,0.0,0.0]
clippingplanes = (5.0,25.0)
viewplane = 7.0
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

#winding_no = 0;

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
        mousex, mousey = pygame.mouse.get_pos()
        
        screen.fill(bgcolor)

        #drawing grid
        pygame.draw.line(screen, grid.xaxis_color, topixel(grid.xaxis.start.x, grid.xaxis.start.y), topixel(grid.xaxis.end.x, grid.xaxis.end.y),2)
        pygame.draw.line(screen, grid.zaxis_color, topixel(grid.zaxis.start.x, grid.zaxis.start.y), topixel(grid.zaxis.end.x, grid.zaxis.end.y),2)
        for edge in grid.edges:
            pygame.draw.line(screen, grid.grid_color, topixel(edge.start.x, edge.start.y), topixel(edge.end.x, edge.end.y),1)
            
        for surfaces in m1.surfaces:
            for edge in surfaces.edges:
                pygame.draw.line(screen, line_color, topixel(edge.start.x, edge.start.y), topixel(edge.end.x, edge.end.y),2)

        
                

    pygame.display.flip()
