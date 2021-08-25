from os import read
from saveData import readModel, saveModel
import pygame
import sys
from graphics_utility import Model, Grid, StandardModels, tonormal, topixel, Vertex, SurfaceSelection
from D3_utility import Camera
from utility_2d import isInterior
import numpy
from pygame.constants import K_LALT, K_LCTRL, K_LSHIFT, K_RALT, K_RCTRL
from TransfClasses import selectAll, changeOrigin
from eventHandlers import *
import time
import settings

screen_yc = settings.Window.height - 5

##selected_surface = None
##selectable_surfaces = []
##selected_surfaces = []

pygame.init()
screen = pygame.display.set_mode(
    (settings.Window.width, settings.Window.height))
pygame.display.set_caption(settings.Window.title)
##bgcolor = (99,99,99)
##line_color = (241,165,5)
##gridcolor = (120, 120, 120)
##zaxiscolor = (28, 217, 44)  #green
##xaxiscolor = (237, 15, 2)  #red
##surfacecolor = (170,170,170)
##selectable_color = (150,150,150)
##selected_color = (200,200,200)
##keyC_color = (100, 100, 0)
##keyFont_color = (0, 0, 0)

#models
grid = Grid(1.0, 10.0, settings.Color.grid, settings.Color.xaxis,
            settings.Color.zaxis)
# m1 = StandardModels().models['cube']
m1 = readModel("sample")

##campos = (10.0,15.0,10.0)
##lookatpos = [0.0,0.0,0.0]
##clippingplanes = (5.0,25.0)
##viewplane = 5.0

#viewing camera
mainCamera = Camera(settings.Camera.campos, settings.Camera.lookatpos,
                    settings.Camera.clippingplanes, settings.Camera.viewplane)
mainCamera.addModel(grid)
mainCamera.addModel(m1)
mainCamera.updateView()

ss = SurfaceSelection()

# font for key command
cmdFont = pygame.font.Font('freesansbold.ttf', 20)

# cmdText = cmdFont.render("hi", True, (0, 0, 0), keyC_color)

# Command window for keyboard commands
keyCommand = CommandWindow(
    settings.Color.keyC,
    pygame.Rect(0, settings.Window.height - 40, settings.Window.width,
                settings.Window.height - 40))

keyP = Command(keyCommand, cmdFont)
# Mouse scroll control
scrollC = mouseScrollControl(ss.selectable_surfaces)

# Mouse position store
##prevMouseX, prevMouseY = pygame.mouse.get_pos()
##mouseX, mouseY = prevMouseX, prevMouseY
##pressed = False

#transforming model to viewing coordinates -------------------------------
##def viewModel():
##    mainCamera.setViewingValues(m1.vertices)
##    for vertex in m1.vertices:
##        v = numpy.array([[vertex.x],
##                         [vertex.y],
##                         [vertex.z],
##                         [1       ]])
##        v = mainCamera.W2Vm.dot(v)
##         # perspective viewing
##        vertex.vx = v[0][0] / v[2][0] * mainCamera.Zvp
##        vertex.vy = v[1][0] / v[2][0] * mainCamera.Zvp
##        vertex.vz = v[2][0]
#-----------------------------------------transforming model to viewing coordinates

#transforming grid ------------------------------------------------------
##def viewGrid():
##    mainCamera.setViewingValues(grid.vertices)
##    for edge in grid.edges:
##        v = numpy.array([[edge.start.x, edge.end.x],
##                         [edge.start.y, edge.end.y],
##                         [edge.start.z, edge.end.z],
##                         [1,            1         ]])
##        v = mainCamera.W2Vm.dot(v)
##        # perspective viewing
##        edge.start.vx = v[0][0] / v[2][0] * mainCamera.Zvp
##        edge.start.vy = v[1][0] / v[2][0] * mainCamera.Zvp
##        edge.end.vx   = v[0][1] / v[2][1] * mainCamera.Zvp
##        edge.end.vy   = v[1][1] / v[2][1] * mainCamera.Zvp
##
##    #for the x and z axis
##    v = numpy.array([[grid.xaxis.start.x, grid.xaxis.end.x, grid.zaxis.start.x, grid.zaxis.end.x],
##                     [grid.xaxis.start.y, grid.xaxis.end.y, grid.zaxis.start.y, grid.zaxis.end.y],
##                     [grid.xaxis.start.z, grid.xaxis.end.z, grid.zaxis.start.z, grid.zaxis.end.z],
##                     [1,                  1,                1,                  1               ]])
##    v = mainCamera.W2Vm.dot(v)
##    grid.xaxis.start.vx = v[0][0] / v[2][0] * mainCamera.Zvp
##    grid.xaxis.start.vy = v[1][0] / v[2][0] * mainCamera.Zvp
##    grid.xaxis.end.vx   = v[0][1] / v[2][1] * mainCamera.Zvp
##    grid.xaxis.end.vy   = v[1][1] / v[2][1] * mainCamera.Zvp
##    grid.zaxis.start.vx = v[0][2] / v[2][2] * mainCamera.Zvp
##    grid.zaxis.start.vy = v[1][2] / v[2][2] * mainCamera.Zvp
##    grid.zaxis.end.vx   = v[0][3] / v[2][3] * mainCamera.Zvp
##    grid.zaxis.end.vy   = v[1][3] / v[2][3] * mainCamera.Zvp
#-------------------------------------------------------------transforming grid

##viewModel()
##viewGrid()
#mainCamera.zoom(m1, 5)
##mousedrag = False
##drag_time_thres = 0.01
while True:
    for event in pygame.event.get():
        #mouseclicked = False
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseclicked = True
            mousex, mousey = pygame.mouse.get_pos()
            mousex, mousey = tonormal(mousex, mousey)
            mouse_point = Vertex(mousex, mousey, 0)

        # KEYBOARD CONTROLS
        if event.type == pygame.KEYDOWN:
            # Application closes if Key 'q' is pressed
            if event.key == pygame.K_q:
                sys.exit()
            elif (pygame.key.get_pressed()[K_LCTRL]
                  or pygame.key.get_pressed()[K_RCTRL]
                  ) and event.key == pygame.K_a:
                selectAll()
            elif (pygame.key.get_pressed()[K_LCTRL]
                  or pygame.key.get_pressed()[K_RCTRL]
                  ) and event.key == pygame.K_s:
                saveModel(m1, "sample")
            # elif (pygame.key.get_pressed()[K_LCTRL]
            #       or pygame.key.get_pressed()[K_RCTRL]
            #       ) and event.key == settings.KbControl.NEWMODEL:
            #     print("Create New Model")
            elif (event.key == settings.KbControl.ORIGINSELECT
                  ) and event.type == pygame.KEYDOWN:
                if keyP.origin:
                    keyP.origin = False
                    print("center origin")
                else:
                    keyP.origin = True
                    print("world origin")
            elif (event.key == settings.KbControl.ZOOMSELECT
                  ) and event.type == pygame.KEYDOWN:
                if settings.Camera.zoom:
                    settings.Camera.zoom = False
                    print("zoom deselected")
                else:
                    settings.Camera.zoom = True
                    print("zoom selected")

            elif event.key == settings.KbControl.MULTIPLESELECT and event.type == pygame.KEYDOWN:
                if keyP.multiselect:
                    keyP.multiselect = False
                    ss.multiselect = False
                    print("multiselect on")
                else:
                    keyP.multiselect = True
                    ss.multiselect = True
                    print("multiselect on")

            else:
                keyP.processKey(event.key, ss.selected_surface, mainCamera, m1,
                                ss.selected_surfaces)

                if keyP.extrude:
                    ss.selected_surface = None
                    ss.selectable_surfaces = []
                    ss.selected_surfaces = []
                    keyP.extrude = False

        # MOUSE CONTROLS

        # move mouse while pressing ALT to pan
##        if (( pygame.key.get_pressed()[K_LALT] or pygame.key.get_pressed()[K_RALT]) and (not pressed)):
##            prevMouseX, prevMouseY = pygame.mouse.get_pos()
##            pressed = True
##        elif (( pygame.key.get_pressed()[K_LALT] or pygame.key.get_pressed()[K_RALT]) and pressed ):
##            mouseX, mouseY = pygame.mouse.get_pos()
##            scrollC.processMovement(prevMouseX, prevMouseY, mouseX, mouseY)
##            if scrollC.movement:
##                mx,my = 0, 0
##                if scrollC.movX != 0:
##                    movx = min(rotate_pixel_amount, abs(scrollC.movX))
##                    mx =  movx * scrollC.movX/abs(scrollC.movX) / screen_xy * rotate_amount
##                if scrollC.movY != 0:
##                    movy = min(rotate_pixel_amount, abs(scrollC.movY))
##                    my = movy * scrollC.movY/abs(scrollC.movY) / screen_xy * rotate_amount
##                v = numpy.array([[mainCamera.x],
##                                 [mainCamera.y],
##                                 [mainCamera.z],
##                                 [1,          ]])
##                up_rot = Transform_matrix.rotate(math.degrees(math.atan(mainCamera.z/mainCamera.x)),'y') .dot(Transform_matrix.rotate(my,'z').dot(
##                                                    Transform_matrix.rotate(-math.degrees(math.atan(mainCamera.z/mainCamera.x)),'y')))
##                v = Transform_matrix.rotate(mx,'y').dot(up_rot.dot(v))
##                mainCamera.x, mainCamera.y, mainCamera.z = v[0][0], v[1][0], v[2][0]
##                mainCamera.constructUVN()
##                viewModel()
##                viewGrid()
##
##            pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == settings.MouseControl.PANBUTTON:
            prevmousex, prevmousey = pygame.mouse.get_pos()
            settings.MouseControl.mousedrag = True
            drag_start = time.time()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == settings.MouseControl.PANBUTTON:
            settings.MouseControl.mousedrag = False
        elif event.type == pygame.MOUSEMOTION and settings.MouseControl.mousedrag == True:
            drag_time = time.time()
            if (drag_time -
                    drag_start) > settings.MouseControl.drag_time_thres:
                drag_start = drag_time
                curmousex, curmousey = pygame.mouse.get_pos()
                movx, movy = curmousex - prevmousex, curmousey - prevmousey
                ##                print(movx, movy)
                prevmousex, prevmousey = curmousex, curmousey
                ##                mx =  movx / screen_xy * rotate_amount
                ##                my = movy / screen_xy * rotate_amount
                mx = movx * settings.Camera.rotation_per_pixel
                my = movy * settings.Camera.rotation_per_pixel
                mainCamera.rotate(mx, my)
##                v = numpy.array([[mainCamera.x],
##                                 [mainCamera.y],
##                                 [mainCamera.z],
##                                 [1,          ]])
####                print(math.degrees(math.atan(mainCamera.z/mainCamera.x)))
##                up_rot = Transform_matrix.rotate(-math.degrees(math.atan(mainCamera.z/mainCamera.x)),'y') .dot(Transform_matrix.rotate(my,'z').dot(
##                                                    Transform_matrix.rotate(math.degrees(math.atan(mainCamera.z/mainCamera.x)),'y')))
##                v = Transform_matrix.rotate(mx,'y').dot(up_rot.dot(v))
##                mainCamera.x, mainCamera.y, mainCamera.z = v[0][0], v[1][0], v[2][0]
##                mainCamera.constructUVN()
##                mainCamera.updateView()
##                viewModel()
##                viewGrid()

# Scoll through list
        if not settings.Camera.zoom:
            if (event.type == pygame.MOUSEBUTTONDOWN) and (
                    event.button == 4
                    or event.button == 5) and scrollC.selectedList:
                scrollC.processEvent(event)
                ss.setSelectedSurface(scrollC.selectedIndex)
        else:
            if (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 4:
                mainCamera.zoom(settings.Camera.zoom_amount * mainCamera.Zvp /
                                10)
            elif (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 5:
                mainCamera.zoom(-settings.Camera.zoom_amount * mainCamera.Zvp /
                                10)

        if ss.multiselect and event.type == pygame.MOUSEBUTTONDOWN and event.button == settings.MouseControl.MULTIPLESELECTASSERT and ss.selected_surface:
            if ss.selected_surface in ss.selected_surfaces:
                ss.selected_surfaces.remove(ss.selected_surface)
            else:
                ss.setSelectedSurfaces()

##        si = 0
##        for surface in m1.surfaces:
##            if checkForPointInside(mouse_point, surface.edges):
##                print("Inside",si)
##            si += 1

        screen.fill(settings.Color.bg)

        #drawing grid
        grid.display(screen)
        ##        pygame.draw.aaline(screen, grid.xaxis_color, topixel(grid.xaxis.start.vx, grid.xaxis.start.vy), topixel(grid.xaxis.end.vx, grid.xaxis.end.vy))
        ##        pygame.draw.aaline(screen, grid.zaxis_color, topixel(grid.zaxis.start.vx, grid.zaxis.start.vy), topixel(grid.zaxis.end.vx, grid.zaxis.end.vy))
        ##
        ##        for edge in grid.edges:
        ##            pygame.draw.aaline(screen, grid.grid_color, topixel(edge.start.vx, edge.start.vy), topixel(edge.end.vx, edge.end.vy))
        ##
        #drawing cube-model ->surface(selected)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == settings.MouseControl.SELECTBUTTON:
            ss.selectable_surfaces.clear()
            for surface in m1.surfaces:
                if isInterior(mouse_point, surface.edges):
                    ss.selectable_surfaces.append(surface)
        if not scrollC.selectedList:
            ss.setSelectedSurface(-1)
        ss.display(screen)

        ##        for surface in selectable_surfaces:
        ##            surface_points = []
        ##            for v in surface.vertices:
        ##                surface_points.append(topixel(v.vx,v.vy))
        ##            pygame.draw.polygon(screen, settings.Color.selectable, surface_points)
        ##        if selected_surface:
        ##            surface_points = []
        ##            for v in selected_surface.vertices:
        ##                surface_points.append(topixel(v.vx,v.vy))
        ##            pygame.draw.polygon(screen, settings.Color.selected, surface_points)

        #drawing cube-model ->edges
        m1.display_wireframe(screen)
        ##        for edge in m1.edges:
        ##            pygame.draw.aaline(screen, line_color, topixel(edge.start.vx, edge.start.vy), topixel(edge.end.vx, edge.end.vy))

        # Command view box
        pygame.draw.rect(screen, keyP.commandWindow.color, keyP.rect)
        screen.blit(
            cmdFont.render("Current Command : " + keyP.getPressedKeysStr(),
                           True, settings.Color.keyFont, settings.Color.keyC),
            keyP.rect)

    pygame.display.flip()
