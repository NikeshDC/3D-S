class Window:
    title = "3DS"
    width = 1200
    height = 800
    # xy = min(width, height)
    xy = 300


class Grid:
    SPAN = 15.0
    SPACING = 1.0


class Shading:
    FLAT = 0
    GOURAUD = 1
    # PHONG = 2
    NUMBER = 2


class MouseControl:
    mousedrag = False
    drag_time_thres = 0.01
    PANBUTTON = 3  #right click
    ZOOMINBUTTON = 4  #scroll up
    ZOOMOUTBUTTON = 5  #scroll down
    SELECTBUTTON = 1  #left click
    MULTIPLESELECTASSERT = 3  #right click


from pygame.constants import K_n, K_w, K_p, K_o


class KbControl:
    MULTIPLESELECT = K_w
    ORIGINSELECT = K_o
    ZOOMSELECT = K_p
    NEWMODEL = K_n


class Camera:
    zoom = True
    Vp = -5.0
    rotation_per_pixel = 0.1
    campos = (10.0, 15.0, 10.0)
    lookatpos = [0.0, 0.0, 0.0]
    clippingplanes = (-5.0, -25.0)
    zoom_amount = 0.5


##    maxdepth_inv = 1 / -100.0
##    z_buffer = [maxdepth_inv for x in range(window_del_x * window_del_y)]


class Light:
    pos = [(2, 7, 2), (-5, 5, 10)]

    intensity = 10
    #direction = ()
    mpv = 250  #maximum pixel value for models
    ia = 0.6  #ambient_intensity
    a0 = 10.0
    #a1 = 1.0
    a2 = 1.0


class Color:
    bg = (99, 99, 99)
    renderedbg = (255, 255, 255)
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
