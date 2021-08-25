from graphics_utility import Vertex, Edge

def get_cross(point1,point2,point3):
    '''returns crossproduct of the edges formed by the vertex listed in order'''
    #(p2-p1).x*(p3-p2).y - (p2-p1).y*(p3-p2).x
    zval = ((point2.vx - point1.vx)*(point3.vy - point2.vy) - (point2.vy - point1.vy)*(point3.vx - point2.vx))
    return zval


def lineIntersects(line1, line2):
    a1 = line1.start
    b1 = line1.end
    a2 = line2.start
    b2 = line2.end
    if(get_cross(a1,b1,a2)*get_cross(a1,b1,b2) <= 0 and get_cross(a2,b2,a1)*get_cross(a2,b2,b1) <= 0):
        return True
    else:
        return False
    
    
def isInterior(point, polygon, max_x = 100):
    '''accepts a vertex and surface and checks if the point lies inside the surface in 2D(xy plane)'''
    scanline = Edge(point, Vertex(max_x,point.y,0))  #scan line to calculate number of times edges of polygon crosses, extending horizantally from 'point' towards infinity(here 'max_x')
    cross_no = 0
    for edge in polygon:
        if (lineIntersects(edge, scanline)):
                cross_no += 1
    if(cross_no%2 == 0):
        return False
    else:
        return True
