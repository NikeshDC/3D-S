import pygame
import sys
from pygame import key
from pygame import fastevent

from pygame.image import save
from graphics_utility import Model, Grid, StandardModels, tonormal, topixel, Vertex, SurfaceSelection, Light
from D3_utility import Camera
from utility_2d import isInterior
import numpy
from pygame.constants import K_DELETE, K_F1, K_LALT, K_LCTRL, K_LSHIFT, K_RALT, K_RCTRL, K_RSHIFT, K_v
from TransfClasses import selectAll, changeOrigin, checkKeys, strManip
from eventHandlers import *
import time
import settings
import saveData

screen_yc = settings.Window.height - 5
rendered_view = False
selected_light = None

pygame.init()
screen = pygame.display.set_mode(
    (settings.Window.width, settings.Window.height))
pygame.display.set_caption(settings.Window.title)

#models
MODEL_BEG = 0
#models = []
grid = Grid(settings.Grid.SPACING, settings.Grid.SPAN, settings.Color.grid,
            settings.Color.xaxis, settings.Color.zaxis)
m1 = StandardModels().models['cube']
m1.shading = settings.Shading.GOURAUD
m1.material.color = (0, 255, 0)
#models.append(m1)
defaultModel = m1
selectedModel = defaultModel
ss = SurfaceSelection()

#viewing camera
mainCamera = Camera(settings.Camera.campos, settings.Camera.lookatpos,
                    settings.Camera.clippingplanes, settings.Camera.Vp)
mainCamera.addModel(grid)
mainCamera.addDisplayObject(
    ss
)  #this order of adding model says that first grid is displayed then ss and then m1
mainCamera.addModel(m1)
for pos in settings.Light.pos:
    l = Light(pos, settings.Light.intensity)
    mainCamera.addLight(l)
mainCamera.updateView()

onePixelToNormal = 2 / settings.Window.xy
window_minx, window_miny = tonormal(1, settings.Window.height - 5)
window_maxx, window_maxy = tonormal(settings.Window.width - 5, 1)

# font for key command
cmdFont = pygame.font.Font('freesansbold.ttf', 20)

# Command window for keyboard commands
keyCommand = CommandWindow(
    settings.Color.keyC,
    pygame.Rect(0, settings.Window.height - 40, settings.Window.width,
                settings.Window.height - 40))

keyP = Command(keyCommand, cmdFont)

# Mouse scroll control
scrollC = mouseScrollControl(ss.selectable_surfaces)
pressedNums = []
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
                mainCamera.z_buffer_rendering(screen, window_minx, window_maxx,
                                              window_miny, window_maxy,
                                              onePixelToNormal)
                pygame.display.flip()
                continue
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mousex, mousey = pygame.mouse.get_pos()
            for light in mainCamera.lights:
                light.selected = False
                selected_light = None

            for light in mainCamera.lights:
                if light.checkPoint():
                    selected_light = light
                    light.selected = True
                    #print("selected")
                    break

            mouse_point = tonormal(mousex, mousey)

        if rendered_view:  #no controls in rendered view
            continue

        # KEYBOARD CONTROLS
        if event.type == pygame.KEYDOWN:
            if (checkKeys.isDigit(event.key)):
                pressedNums.append(event.key)
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
                saveData.saveAll(mainCamera)

            elif (pygame.key.get_pressed()[K_v]
                  and checkKeys.isDigit(event.key)):
                print("Read model", strManip.makeStr(pressedNums))
                saveData.readAll(mainCamera,
                                 int(strManip.makeStr(pressedNums)), MODEL_BEG)
                pressedNums.clear()
                keyP.pressedKeys.clear()
            elif (event.key == pygame.K_TAB):
                if ss.selected_surface:
                    mainCamera.lookat((ss.selected_surface.center.x,
                                       ss.selected_surface.center.y,
                                       ss.selected_surface.center.z))

            # CTRL + n FOR SAVING MODEL
            elif (pygame.key.get_pressed()[K_LCTRL]
                  or pygame.key.get_pressed()[K_RCTRL]) and checkKeys.isDigit(
                      event.key):
                print("Save model", pressedNums)
                saveData.saveModel(selectedModel,
                                   strManip.makeStr(pressedNums))
                pressedNums.clear()
                keyP.pressedKeys.clear()
            elif event.key == K_DELETE and selectedModel:

                mainCamera.display_objects.remove(selectedModel)
                mainCamera.models.remove(selectedModel)
                selectedModel = None
                ss.selected_surface = None
                ss.selectable_surfaces.clear()
                ss.selected_surfaces.clear()
            elif event.key == K_F1 and selectedModel:
                selectedModel.shading += 1
                selectedModel.shading %= settings.Shading.NUMBER
            # SHIFT + n FOR SELECTING MODEL
            elif (pygame.key.get_pressed()[K_LSHIFT]
                  or pygame.key.get_pressed()[K_RSHIFT]) and checkKeys.isDigit(
                      event.key):
                print("select model", strManip.makeStr(pressedNums))
                mcount = -1
                for model in mainCamera.models:
                    if isinstance(model, Model):
                        mcount = mcount + 1
                        if (mcount == int(strManip.makeStr(pressedNums))):
                            selectedModel = model
                            break
                pressedNums.clear()
                keyP.pressedKeys.clear()

            # ALT + N FOR READING/PLACING MODEL
            elif (pygame.key.get_pressed()[K_LALT]
                  or pygame.key.get_pressed()[K_RALT]) and checkKeys.isDigit(
                      event.key):
                print("Read model", strManip.makeStr(pressedNums))
                m = saveData.readModel(strManip.makeStr(pressedNums))
                mainCamera.addModel(m)
                mainCamera.updateView()
                pressedNums.clear()
                keyP.pressedKeys.clear()
            # ALT + N FOR READING/PLACING MODEL
            elif (pygame.key.get_pressed()[K_LALT]
                  or pygame.key.get_pressed()[K_RALT]
                  ) and event.key == pygame.K_n:

                m = StandardModels().models['cube']
                mainCamera.addModel(m)
                mainCamera.updateView()

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
                    print("multiselect off")
                else:
                    keyP.multiselect = True
                    ss.multiselect = True
                    print("multiselect on")
            else:

                keyP.processKey(event.key, ss.selected_surface, mainCamera,
                                selectedModel, ss.selected_surfaces,
                                pressedNums)

                if keyP.extrude:
                    ss.selected_surface = None
                    ss.selectable_surfaces = []
                    ss.selected_surfaces = []
                    keyP.extrude = False

                elif keyP.light_translate and selected_light:
                    tdir = transformationVals.LTranslateC.getDirection()
                    if tdir == 'x':
                        tx, ty, tz = transformationVals.LTranslateC.getTranslVal(
                        ), 0, 0
                    elif tdir == 'y':
                        tx, ty, tz = 0, transformationVals.LTranslateC.getTranslVal(
                        ), 0
                    elif tdir == 'z':
                        tx, ty, tz = 0, 0, transformationVals.LTranslateC.getTranslVal(
                        )
                    selected_light.translate(tx, ty, tz, mainCamera)
                    keyP.light_translate = False
                elif keyP.light_rotate and selected_light:
                    rdir = transformationVals.LRotateC.getDirection()
                    rang = transformationVals.LRotateC.getAngle()
                    selected_light.rotate(rang, rdir, mainCamera)
                    keyP.light_rotate = False
                elif keyP.light_intensity and selected_light:
                    selected_light.setIntensity(
                        transformationVals.lightIntensity)
                    keyP.light_intensity = False
                elif keyP.material_color and selectedModel:
                    selectedModel.material.setColor(mat.color[0], mat.color[1],
                                                    mat.color[2])
                    keyP.material_color = False
                    print("model no.:", mainCamera.models.index(selectedModel))
                elif keyP.material_ambient and selectedModel:
                    selectedModel.material.setKa(mat.ambient)
                    keyP.material_ambient = False
                elif keyP.material_diffuse and selectedModel:
                    selectedModel.material.setKd(mat.diffuse)
                    keyP.material_diffuse = False
                elif keyP.material_specular_radius and selectedModel:
                    selectedModel.material.setNs(mat.specRadius)
                    keyP.material_specular_radius = False
                elif keyP.material_specular_constant and selectedModel:
                    selectedModel.material.setKs(mat.specConstant)
                    keyP.material_specular_constant = False

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
                prevmousex, prevmousey = curmousex, curmousey
                mx = movx * settings.Camera.rotation_per_pixel
                my = movy * settings.Camera.rotation_per_pixel
                mainCamera.rotate(-mx, my)

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

        screen.fill(settings.Color.bg)

        # drawing cube-model

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == settings.MouseControl.SELECTBUTTON:
            ss.selectable_surfaces.clear()
            if selectedModel:
                for surface in selectedModel.surfaces:
                    if isInterior(mouse_point, surface.edges):
                        ss.selectable_surfaces.append(surface)
        if not scrollC.selectedList:
            ss.setSelectedSurface(-1)

        mainCamera.display(screen)

        # Command view box
        pygame.draw.rect(screen, keyP.commandWindow.color, keyP.rect)
        screen.blit(
            cmdFont.render("Current Command : " + keyP.getPressedKeysStr(),
                           True, settings.Color.keyFont, settings.Color.keyC),
            keyP.rect)

    pygame.display.flip()
