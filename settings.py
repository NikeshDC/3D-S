##class View:
##    models = []
##
##
##    WORLD = 0
##    CENTER = 1
##    origin = WORLD
##    multiselect = False


class Window:
    title = "3DS"
    width = 1100
    height = 700
    xy = min(width, height)


class MouseControl:
    mousedrag = False
    drag_time_thres = 0.01
    PANBUTTON = 3  #middle mouse button
    ZOOMINBUTTON = 4  #scroll up
    ZOOMOUTBUTTON = 5  #scroll down
    SELECTBUTTON = 1  #left click
    MULTIPLESELECTASSERT = 2  #right click


from pygame import K_m, K_o, K_p
from pygame.constants import K_n, K_w


class KbControl:
    MULTIPLESELECT = K_w
    ORIGINSELECT = K_o
    ZOOMSELECT = K_p
    NEWMODEL = K_n


class Camera:
    zoom = True
    cameraVp = 5.0
    rotation_per_pixel = 0.1
    campos = (10.0, 15.0, 10.0)
    lookatpos = [0.0, 0.0, 0.0]
    clippingplanes = (5.0, 25.0)
    viewplane = 5.0
    zoom_amount = 0.5


class Color:
    bg = (99, 99, 99)
    wireframe = (241, 165, 5)
    grid = (120, 120, 120)
    zaxis = (28, 217, 44)  #green
    xaxis = (237, 15, 2)  #red
    selectable = (150, 150, 150)
    selected = (200, 200, 200)
    multiselect = (175, 175, 175)
    keyC = (100, 100, 0)
    keyFont = (0, 0, 0)


##class Transformation:
##    rotate = False
##    scale = False
##    translate = False
##    extrude = False
##    inset = False
