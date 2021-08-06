import pygame
import sys
from graphics_utility import *
from D3_utility import *
from utility_2d import *
import numpy
from pygame.constants import K_LALT, K_LCTRL, K_LSHIFT, K_RALT, K_RCTRL
from TransfClasses import selectAll, changeOrigin
from eventHandlers import *

import warnings
warnings.filterwarnings("ignore", category=numpy.VisibleDeprecationWarning)


rotate_amount = 10
rotate_pixel_amount = 50
screen_x = 1100
screen_y = 700
#account for different dimensions of screen width and height to draw proportionately
screen_xy = min(screen_x,screen_y)

screen_yc = screen_y - 5

# Orign toggler
orgSel = ORIGIN

selected_surface = None
selectable_surfaces = []
selected_surfaces = []


def topixel(x,y):
    '''converts normalized value to actual pixel values'''
    x = int((screen_x + x*screen_xy)/2)
    y = int((screen_y + y*screen_xy)/2)
    return (x,y)

def tonormal(x,y):
    '''converts pixel value to normalized value'''
    x = float((2*x - screen_x)/screen_xy)
    y = float((2*y - screen_y)/screen_xy)
    return (x,y)

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("3Ds")
bgcolor = (99,99,99)
line_color = (241,165,5)
gridcolor = (120, 120, 120)
zaxiscolor = (28, 217, 44)  #green
xaxiscolor = (237, 15, 2)  #red
surfacecolor = (170,170,170)
selectable_color = (150,150,150)
selected_color = (200,200,200)
keyC_color = (100, 100, 0)
keyFont_color = (0, 0, 0)

grid = Grid(1.0,10.0,gridcolor, xaxiscolor, zaxiscolor)
m1 = StandardModels().models['cube']


campos = (10.0,15.0,10.0)
lookatpos = [0.0,0.0,0.0]
clippingplanes = (5.0,25.0)
viewplane = 5.0
mainCamera = Camera(campos,lookatpos, clippingplanes, viewplane)

##m1.translate(1.0,0.0,1.0)
##m1.surfaces[0].scale_center(2.0,2.0,2.0,mainCamera)
###m1.surfaces[0].rotate_center(45.0,'z',mainCamera)
####m1.surfaces[0].rotate_center(-45.0,'z',mainCamera)
###m1.surfaces[0].rotate_center(45.0,'y',mainCamera)
##m1.surfaces[0].translate(-1.0,0.0,0.0,mainCamera)
##m1.extrude(m1.surfaces[0],1,'n',mainCamera)
###m1.surfaces[-1].rotate_center(45.0,'z',mainCamera)
###m1.surfaces[-1].translate(0,1,0,mainCamera)


# font for key command
cmdFont = pygame.font.Font('freesansbold.ttf', 20)

# cmdText = cmdFont.render("hi", True, (0, 0, 0), keyC_color)

# Command window for keyboard commands
keyCommand = CommandWindow(
    keyC_color, pygame.Rect(0, screen_yc - 40, screen_x, screen_yc - 40))

keyP = Command(keyCommand, cmdFont)
# Mouse scroll control
scrollC = mouseScrollControl(selectable_surfaces)

# Mouse position store
prevMouseX, prevMouseY = pygame.mouse.get_pos()
mouseX, mouseY = prevMouseX, prevMouseY
pressed = False


#transforming model to viewing coordinates -------------------------------
def viewModel():
    for vertex in m1.vertices:
        v = numpy.array([[vertex.x],
                         [vertex.y],
                         [vertex.z],
                         [1       ]])
        v = mainCamera.W2Vm.dot(v)
         # perspective viewing
        vertex.vx = v[0] / v[2] * mainCamera.Zvp
        vertex.vy = v[1] / v[2] * mainCamera.Zvp
##    vertex.x = v[0] 
##    vertex.y = v[1]
##    vertex.z = v[2]
##m1.setPlaneCoeffs()
##zx = 0
##for surface in m1.surfaces:
##    zx+=1
##    if surface.c <= 0 :
##        #m1.surfaces.remove(surface)
##        print(zx)
##for vertex in m1.vertices:
##    # perspective viewing
####    vertex.x = v[0] / v[2] * mainCamera.Zvp
####    vertex.y = v[1] / v[2] * mainCamera.Zvp
##    vertex.x = vertex.x / vertex.z * mainCamera.Zvp
##    vertex.y = vertex.y / vertex.z * mainCamera.Zvp
#-----------------------------------------transforming model to viewing coordinates

    

#transforming grid ------------------------------------------------------
def viewGrid():
    for edge in grid.edges:
        v = numpy.array([[edge.start.x, edge.end.x],
                         [edge.start.y, edge.end.y],
                         [edge.start.z, edge.end.z],
                         [1,            1         ]])
        v = mainCamera.W2Vm.dot(v)
        # perspective viewing
        edge.start.vx = v[0][0] / v[2][0] * mainCamera.Zvp
        edge.start.vy = v[1][0] / v[2][0] * mainCamera.Zvp
        edge.end.vx   = v[0][1] / v[2][1] * mainCamera.Zvp
        edge.end.vy   = v[1][1] / v[2][1] * mainCamera.Zvp

    #for the x and z axis
    v = numpy.array([[grid.xaxis.start.x, grid.xaxis.end.x, grid.zaxis.start.x, grid.zaxis.end.x],
                     [grid.xaxis.start.y, grid.xaxis.end.y, grid.zaxis.start.y, grid.zaxis.end.y],
                     [grid.xaxis.start.z, grid.xaxis.end.z, grid.zaxis.start.z, grid.zaxis.end.z],
                     [1,                  1,                1,                  1               ]])
    v = mainCamera.W2Vm.dot(v)
    grid.xaxis.start.vx = v[0][0] / v[2][0] * mainCamera.Zvp
    grid.xaxis.start.vy = v[1][0] / v[2][0] * mainCamera.Zvp
    grid.xaxis.end.vx   = v[0][1] / v[2][1] * mainCamera.Zvp
    grid.xaxis.end.vy   = v[1][1] / v[2][1] * mainCamera.Zvp
    grid.zaxis.start.vx = v[0][2] / v[2][2] * mainCamera.Zvp
    grid.zaxis.start.vy = v[1][2] / v[2][2] * mainCamera.Zvp
    grid.zaxis.end.vx   = v[0][3] / v[2][3] * mainCamera.Zvp
    grid.zaxis.end.vy   = v[1][3] / v[2][3] * mainCamera.Zvp
#-------------------------------------------------------------transforming grid

viewModel()
viewGrid()

while True:
    mouseclicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseclicked = True
            mousex, mousey = pygame.mouse.get_pos()
            mousex, mousey = tonormal(mousex, mousey)
            mouse_point = Vertex(mousex,mousey,0)


        # KEYBOARD CONTROLS
        if event.type == pygame.KEYDOWN:
            # Application closes if Key 'q' is pressed
            if event.key == pygame.K_q:
                sys.exit()
            elif (pygame.key.get_pressed()[K_LCTRL]
                  or pygame.key.get_pressed()[K_RCTRL]
                  ) and event.key == pygame.K_a:
                selectAll()
            elif (event.key == pygame.K_o):
                orgSel = changeOrigin(orgSel)
            elif (event.key == (pygame.K_LALT)
                  or (event.key == pygame.K_RALT)):
                pass
            else:
                keyP.processKey(event.key, selected_surface, mainCamera, m1)

        # MOUSE CONTROLS

        # move mouse while pressing ALT to pan
        if (# event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1) and (
                pygame.key.get_pressed()[K_LALT]
                or pygame.key.get_pressed()[K_RALT]) and (not pressed):
            prevMouseX, prevMouseY = pygame.mouse.get_pos()
            pressed = True
        elif (#event.type == pygame.MOUSEBUTTONUP) and (event.button == 1) and (
                pygame.key.get_pressed()[K_LALT]
                or pygame.key.get_pressed()[K_RALT]) and pressed:
            mouseX, mouseY = pygame.mouse.get_pos()
            scrollC.processMovement(prevMouseX, prevMouseY, mouseX, mouseY)
            if scrollC.movement and scrollC.movX != 0 :
                mx = rotate_pixel_amount * scrollC.movX/abs(scrollC.movX) / screen_xy * rotate_amount
##                mx,my = tonormal(scrollC.movX, scrollC.movY)
##                mx,my = mx * rotate_amount, my * rotate_amount
                v = numpy.array([[mainCamera.x],
                                 [mainCamera.y],
                                 [mainCamera.z],
                                 [1,          ]])
                v = Transform_matrix.rotate(mx,'y').dot(v)
                mainCamera.x, mainCamera.y, mainCamera.z = v[0][0], v[1][0], v[2][0]
                mainCamera.constructUVN()
                viewModel()
                viewGrid()
                
            pressed = False

        # Scoll through list
        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 4 or event.button == 5) and scrollC.selectedList:
            scrollC.processEvent(event)
            selected_surface = scrollC.selectedList[scrollC.selectedIndex]
        

##        si = 0
##        for surface in m1.surfaces:
##            if checkForPointInside(mouse_point, surface.edges):
##                print("Inside",si)
##            si += 1
            
        
        screen.fill(bgcolor)

        #drawing grid
        pygame.draw.aaline(screen, grid.xaxis_color, topixel(grid.xaxis.start.vx, grid.xaxis.start.vy), topixel(grid.xaxis.end.vx, grid.xaxis.end.vy))
        pygame.draw.aaline(screen, grid.zaxis_color, topixel(grid.zaxis.start.vx, grid.zaxis.start.vy), topixel(grid.zaxis.end.vx, grid.zaxis.end.vy))
##        gz_xs,gz_ys = topixel(grid.zaxis.start.x, grid.zaxis.start.y)
##        gz_xe,gz_ye = topixel(grid.zaxis.end.x, grid.zaxis.end.y)
##        pygame.gfxdraw.line(screen, gz_xs, gz_ys, gz_xe, gz_ye, grid.zaxis_color)
        for edge in grid.edges:
            #pygame.draw.line(screen, grid.grid_color, topixel(edge.start.x, edge.start.y), topixel(edge.end.x, edge.end.y),1)
            pygame.draw.aaline(screen, grid.grid_color, topixel(edge.start.vx, edge.start.vy), topixel(edge.end.vx, edge.end.vy))
##
        #drawing cube-model ->surface(selected)
        if mouseclicked:
            selectable_surfaces = []
            for surface in m1.surfaces:
                if isInterior(mouse_point, surface.edges):
                    selectable_surfaces.append(surface)
            scrollC.selectedList = selectable_surfaces
        for surface in selectable_surfaces:
            surface_points = []
            for v in surface.vertices:
                surface_points.append(topixel(v.vx,v.vy))
            pygame.draw.polygon(screen, selectable_color, surface_points)
        if selected_surface:
            surface_points = []
            for v in selected_surface.vertices:
                surface_points.append(topixel(v.vx,v.vy))
            pygame.draw.polygon(screen, selected_color, surface_points)
            
        #drawing cube-model ->edges
        for edge in m1.edges:
            #for edge in surface.edges:
            pygame.draw.aaline(screen, line_color, topixel(edge.start.vx, edge.start.vy), topixel(edge.end.vx, edge.end.vy))

        # Command view box
        pygame.draw.rect(screen, keyP.commandWindow.color, keyP.rect)
        screen.blit(cmdFont.render("Current Command : " + keyP.getPressedKeysStr(), True,
                           keyFont_color, keyC_color), keyP.rect)

    pygame.display.flip()
