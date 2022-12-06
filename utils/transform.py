from utils.general import AppWidth, AppHeight
def im2grid(ix, iy):
    '''
    transform the 2d point cord from image cord to grid cord
    input:ix, iy: x and y position in image cord
    output: x, y: x and y position in grid cord
    '''
    x = ix - AppHeight
    y = AppWidth/2 - iy
    return x, y

def grid2im(x, y):
    '''
    transform the 2d point cord from grid cord to image cord
    input: x, y: x and y position in grid cord
    outpu:ix, iy: x and y position in image cord
    '''
    ix = x + AppHeight
    iy = AppWidth/2 - y 
    return ix, iy
