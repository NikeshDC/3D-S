##def get_cross(point1,point2,point3):
##    '''returns crossproduct of the edges formed by the points listed in order'''
##    #(p2-p1).x*(p3-p2).y - (p2-p1).y*(p3-p2).x
##    zval = (point2[0] - point1[0])*(point3[1] - point2[1]) - (point2[1] - point1[1])*(point3[0] - point2[0])
##    print(zval)
##    return zval;

from graphics_utility import Vertex, Edge

def get_cross(point1,point2,point3):
    '''returns crossproduct of the edges formed by the vertex listed in order'''
    #(p2-p1).x*(p3-p2).y - (p2-p1).y*(p3-p2).x
    zval = ((point2.vx - point1.vx)*(point3.vy - point2.vy) - (point2.vy - point1.vy)*(point3.vx - point2.vx))
    #print(zval, end = " ")
    return zval;

##def lineIntersects(line1, line2):
##    a1 = line1[0];
##    b1 = line1[1];
##    a2 = line2[0];
##    b2 = line2[1];
##    if(get_cross(a1,b1,a2)*get_cross(a1,b1,b2) < 0 and get_cross(a2,b2,a1)*get_cross(a2,b2,b1) < 0):
##        return True
##    else:
##        return False

def lineIntersects(line1, line2):
    a1 = line1.start;
    b1 = line1.end;
    a2 = line2.start;
    b2 = line2.end;
    #print("lineIns")
    if(get_cross(a1,b1,a2)*get_cross(a1,b1,b2) <= 0 and get_cross(a2,b2,a1)*get_cross(a2,b2,b1) <= 0):
        #print("lineIne")
        return True
    else:
        #print("lineIne")
        return False
    
##def chechForPointInside(point, polygon, max_x = 1000):
##    '''accepts a point and list of edges representing polygon and checks if the point lies inside the polygon'''
##    if len(polygon) < 3:
##        print("not sufficient points for polygon")
##        return
##
##    scanline = ((max_x,point[1]),(point[0],point[1]))  #scan line to calculate winding no extending horizantally from point towards infinity(here max_x)
##    winding_no = 0
##    for edge in polygon:
##        if (lineIntersects(edge, scanline)):
##            if(edge[0][1] < edge[1][1]):    #check direction of edge withrespect to the horizantal scan line
##                winding_no += 1
##            else:
##                winding_no -= 1
##
##    if(winding_no == 0):
##        return False
##    else:
##        return True

def isInterior(point, polygon, max_x = 100):
    '''accepts a vertex and surface and checks if the point lies inside the surface in 2D(xy plane)'''
    scanline = Edge(point, Vertex(max_x,point.y,0))  #scan line to calculate number of times edges of polygon crosses, extending horizantally from point towards infinity(here max_x)
    cross_no = 0
    for edge in polygon:
        if (lineIntersects(edge, scanline)):
                cross_no += 1
    #print("w:",cross_no)
    if(cross_no%2 == 0):
        return False
    else:
        return True
