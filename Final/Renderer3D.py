import pygame
from Math import *
from Window import *

#draw_texture_tri(src[3][2],dest[3][2], texture)
#src : source texture coordinates (u, v)
#dest : destination screen coordinates (x, y)
def draw_texture_tri(src, dest, texture):
    # Extract source and destination points
    (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2) = src
    (dest_x2, dest_y2), (dest_x0, dest_y0), (dest_x1, dest_y1),  = dest
    
    # Get the texture size
    tex_w, tex_h = texture.get_size()
    
    # Get the texture data
    data_array = pygame.surfarray.pixels3d(texture)
    
    # Calculate the area of the triangle
    area = (dest_x1 - dest_x0) * (dest_y2 - dest_y0) - (dest_x2 - dest_x0) * (dest_y1 - dest_y0)
    
    # Loop through the bounding box of the triangle
    mini1 = min(dest_y0, dest_y1, dest_y2)
    mini2 = min(dest_x0, dest_x1, dest_x2)
    maxi1 = max(dest_y0, dest_y1, dest_y2)
    maxi2 = max(dest_x0, dest_x1, dest_x2)
    #TODO: Fix the clipping
    mini1 = clamp(mini1, 0, Window.Instance.height)
    mini2 = clamp(mini2, 0, Window.Instance.width)
    maxi1 = clamp(maxi1, 0, Window.Instance.height)
    maxi2 = clamp(maxi2, 0, Window.Instance.width)
    ############
    for y in range(mini1, maxi1):
        for x in range(mini2, maxi2):
            # Calculate the barycentric coordinates
            if area == 0:
                continue
            w0 = ((dest_x1 - dest_x0) * (y - dest_y0) - (dest_y1 - dest_y0) * (x - dest_x0)) / area
            w1 = ((dest_x2 - dest_x1) * (y - dest_y1) - (dest_y2 - dest_y1) * (x - dest_x1)) / area
            w2 = 1 - w0 - w1
            
            # Check if the point is inside the triangle
            if 0 <= w0 <= 1 and 0 <= w1 <= 1 and 0 <= w2 <= 1:
                # Calculate the texture coordinates
                u = w0 * src_x0 + w1 * src_x1 + w2 * src_x2
                v = w0 * src_y0 + w1 * src_y1 + w2 * src_y2
                u = int(u) % tex_w
                v = int(v) % tex_h
                
                # Get the color from the texture and draw it on the screen
                color = data_array[u, v]
                Window.Instance.surface.set_at((x, y), color)


def draw_texture_quad(src, dest, texture):
    # Extract source and destination points
    top_left, top_right, bottom_right, bottom_left = src
    top_left_dest, top_right_dest, bottom_right_dest, bottom_left_dest = dest
    
    # Draw the two triangles that form the quad
    draw_texture_tri((top_left, bottom_right, bottom_left), (top_left_dest, bottom_right_dest, bottom_left_dest), texture)
    draw_texture_tri((top_left, top_right, bottom_right), (top_left_dest, top_right_dest, bottom_right_dest), texture)

class TriangleDrawer:
    Buffer = []
    def __init__(self, texture, src, dest, depth):
        self.texture = texture
        self.src = src
        self.dest = dest
        self.depth = depth
    
    @staticmethod
    def SortBuffer():
        TriangleDrawer.Buffer.sort(key=lambda td: td.depth, reverse=True)

    @staticmethod
    def DrawBuffer():
        for tri in TriangleDrawer.Buffer:
            draw_texture_tri(tri.src, tri.dest, tri.texture)

    @staticmethod
    def ClearBuffer():
        TriangleDrawer.Buffer = []

def QuadDrawerAppend(src, dest, texture, depth):
    top_left, top_right, bottom_right, bottom_left = src
    top_left_dest, top_right_dest, bottom_right_dest, bottom_left_dest = dest

    src = (top_left, bottom_right, bottom_left)
    dest = (top_left_dest, bottom_right_dest, bottom_left_dest)
    TriangleDrawer.Buffer.append(TriangleDrawer(texture, src, dest, depth))
    src = (top_left, top_right, bottom_right)
    dest = (top_left_dest, top_right_dest, bottom_right_dest)
    TriangleDrawer.Buffer.append(TriangleDrawer(texture, src, dest, depth))

def TriangleDrawerAppend(src, dest, texture, depth):
    TriangleDrawer.Buffer.append(TriangleDrawer(texture, src, dest, depth))