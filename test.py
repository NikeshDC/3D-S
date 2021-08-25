import pygame
import sys
from graphics_utility import Model, Grid, StandardModels, tonormal, topixel, Vertex, SurfaceSelection, Light
from D3_utility import Camera
from utility_2d import isInterior
import numpy
from pygame.constants import K_LALT, K_LCTRL, K_LSHIFT, K_RALT, K_RCTRL
from TransfClasses import selectAll, changeOrigin
from eventHandlers import *
import time
import settings
import saveData



screen_yc = settings.Window.height - 5
rendered_view = False
selected_light = None

pygame.init()
screen = pygame.display.set_mode((settings.Window.width, settings.Window.height))
pygame.display.set_caption(settings.Window.title)

#models
#models = []
grid = Grid(1.0,10.0,settings.Color.grid, settings.Color.xaxis, settings.Color.zaxis)
m1 = StandardModels().models['cube']
m1.shading = settings.Shading.GOURAUD
m1.material.color = (0, 255, 0)
#models.append(m1)

ss = SurfaceSelection()
l1 = Light(settings.Light.pos, settings.Light.intensity)

#viewing camera
mainCamera = Camera(settings.Camera.campos, settings.Camera.lookatpos, settings.Camera.clippingplanes, settings.Camera.Vp)
mainCamera.addModel(grid)
mainCamera.addDisplayObject(ss)  #this order of adding model says that first grid is displayed then ss and then m1
mainCamera.addModel(m1)
mainCamera.addLight(l1)
mainCamera.updateView()

onePixelToNormal = 2 / settings.Window.xy
window_minx, window_miny = tonormal(0, settings.Window.height)
window_maxx, window_maxy = tonormal(settings.Window.width, 0)

# font for key command
cmdFont = pygame.font.Font('freesansbold.ttf', 20)

# Command window for keyboard commands
keyCommand = CommandWindow(
    settings.Color.keyC, pygame.Rect(0, settings.Window.height - 40, settings.Window.width, settings.Window.height - 40))

keyP = Command(keyCommand, cmdFont)
# Mouse scroll control
scrollC = mouseScrollControl(ss.selectable_surfaces)


while True:
    for event in pygame.event.get():
        #mouseclicked = False
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if rendered_view:
                rendered_view = False
            else:
                rendered_view = True
                screen.fill(settings.Color.renderedbg)
                mainCamera.z_buffer_rendering(screen, window_minx, window_maxx, window_miny, window_maxy, onePixelToNormal)
                pygame.display.flip()
                continue
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousex, mousey = pygame.mouse.get_pos()
            for light in mainCamera.lights:
                if light.checkPoint():
                    selected_light = light
                    light.selected = True
                    #print("selected")
                    break
                else:
                    light.selected = False
                    selected_light = None
            mouse_point = tonormal(mousex, mousey)
            
        if rendered_view: #no controls in rendered view
            continue

        # KEYBOARD CONTROLS
        if event.type == pygame.KEYDOWN:
            # Application closes if Key 'q' is pressed
            if event.key == pygame.K_q:
                sys.exit()
            elif (pygame.key.get_pressed()[K_LCTRL]
                  or pygame.key.get_pressed()[K_RCTRL]
                  ) and event.key == pygame.K_a:
                selectAll()
            elif (event.key == settings.KbControl.ORIGINSELECT):
                if keyP.origin:
                    keyP.origin = False
                    print("center origin")
                else:
                    keyP.origin = True
                    print("world origin")
            elif (event.key == settings.KbControl.ZOOMSELECT):
                if settings.Camera.zoom:
                    settings.Camera.zoom = False
                    print("zoom deselected")
                else:
                    settings.Camera.zoom = True
                    print("zoom selected")
            elif event.key == settings.KbControl.MULTIPLESELECT:
                if keyP.multiselect:
                    keyP.multiselect = False
                    ss.multiselect = False
                    print("multiselect on")
                else:
                    keyP.multiselect = True
                    ss.multiselect = True
                    print("multiselect on")
            elif event.key == pygame.K_w:
                saveData.saveModel(m1,"sss")
            elif event.key >= pygame.K_1 and event.key <= pygame.K_9 and len(keyP.pressedKeys) == 0:
                print(pygame.key.name(event.key))
            else:
                keyP.processKey(event.key, ss.selected_surface, mainCamera, m1, ss.selected_surfaces)

                if keyP.extrude:
                    ss.selected_surface = None
                    ss.selectable_surfaces = []
                    ss.selected_surfaces = []
                    keyP.extrude = False

                elif keyP.light_translate and selected_light:
                    tdir = transformationVals.LTranslateC.getDirection()
                    if tdir == 'x':
                        tx, ty, tz = transformationVals.LTranslateC.getTranslVal(), 0, 0
                    elif tdir == 'y':
                        tx, ty, tz = 0, transformationVals.LTranslateC.getTranslVal(), 0
                    elif tdir == 'z':
                        tx, ty, tz = 0, 0, transformationVals.LTranslateC.getTranslVal()
                    selected_light.translate(tx,ty,tz, mainCamera)
                    keyP.light_translate = False
                elif keyP.light_rotate and selected_light:
                    rdir = transformationVals.LRotateC.getDirection()
                    rang = transformationVals.LRotateC.getAngle()
                    selected_light.rotate(rang, rdir, mainCamera)
                    keyP.light_rotate = False
        


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == settings.MouseControl.PANBUTTON:
            prevmousex, prevmousey =  pygame.mouse.get_pos()
            settings.MouseControl.mousedrag = True
            drag_start = time.time()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == settings.MouseControl.PANBUTTON:
            settings.MouseControl.mousedrag = False
        elif event.type == pygame.MOUSEMOTION and settings.MouseControl.mousedrag == True:
            drag_time = time.time()
            if (drag_time - drag_start) > settings.MouseControl.drag_time_thres:
                drag_start = drag_time
                curmousex, curmousey =  pygame.mouse.get_pos()
                movx, movy = curmousex - prevmousex, curmousey - prevmousey
                prevmousex, prevmousey = curmousex, curmousey
                mx = movx * settings.Camera.rotation_per_pixel
                my = movy * settings.Camera.rotation_per_pixel
                mainCamera.rotate(-mx,my)


        # Scoll through list
        if not settings.Camera.zoom:
            if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 4 or event.button == 5) and scrollC.selectedList:
                scrollC.processEvent(event)
                ss.setSelectedSurface(scrollC.selectedIndex)
        else:
            if (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 4:
                mainCamera.zoom(settings.Camera.zoom_amount * mainCamera.Zvp / 10)
            elif (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 5:
                mainCamera.zoom(-settings.Camera.zoom_amount * mainCamera.Zvp / 10)
            

        if ss.multiselect and event.type == pygame.MOUSEBUTTONDOWN and event.button == settings.MouseControl.MULTIPLESELECTASSERT and ss.selected_surface:
            if ss.selected_surface in ss.selected_surfaces:
                ss.selected_surfaces.remove(ss.selected_surface)
            else:
                ss.setSelectedSurfaces()


        screen.fill(settings.Color.bg)

        #drawing cube-model ->surface(selected)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == settings.MouseControl.SELECTBUTTON:
            ss.selectable_surfaces.clear()
            for surface in m1.surfaces:
                if isInterior(mouse_point, surface.edges):
                    ss.selectable_surfaces.append(surface)
        if not scrollC.selectedList:
            ss.setSelectedSurface(-1)
            
        mainCamera.display(screen)
        
        # Command view box
        pygame.draw.rect(screen, keyP.commandWindow.color, keyP.rect)
        screen.blit(cmdFont.render("Current Command : " + keyP.getPressedKeysStr(), True,
                           settings.Color.keyFont, settings.Color.keyC), keyP.rect)
        
    pygame.display.flip()

