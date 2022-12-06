from numpy import sqrt as sqrt
####Geometry settings
AB = 150
BC = 100
CD = 50
GridWidth = 600
GridHeight = 300

def CalculatePointC(BC, CD, BD, bx, by, dx, dy):
    '''
    Given the two points of a triangle, calculate the location of the third point
    http://paulbourke.net/geometry/circlesphere/
    input:
    BC, CD, BD: length of the three lines of the triangle
    bx, by, dx, dy: x, y location of point b, and point d
    output: True/False, and a list contains x, and y location of the third point
    '''
    a = (BC**2 - CD**2 + BD**2) / (2 * BD+0.00001)
    h = sqrt(max(BC**2 - a**2, 0))
    tempx = bx + a *(dx-bx) / (BD+0.00001)
    tempy = by + a *(dy-by) / (BD+0.00001)
    cx =  tempx + h*(dy-by) / (BD+0.00001)
    cy =  tempy - h*(dx-bx) / (BD+0.00001)
    PointCList = []
    isValid = False
    if cy >= 0:
        PointCList.append([cx, cy])
        isValid = True
    cx =  tempx - h*(dy-by) / (BD+0.00001)
    cy =  tempy + h*(dx-bx) / (BD+0.00001)
    if cy >= 0:
        PointCList.append([cx, cy])
        isValid = True
    return isValid, PointCList