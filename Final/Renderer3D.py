import pygame
from Math import *
from Window import *

import numpy as np

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def is_backfacing(dest):
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = dest
    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0) < 0

def draw_texture_trapezoid(src, dest, texture, backface_culling=True):
    (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2) = src
    (dest_x0, dest_y0, dest_z0), (dest_x1, dest_y1, dest_z1), (dest_x2, dest_y2, dest_z2) = dest
    
    # Get the texture size
    tex_w, tex_h = texture.get_size()
    
    if backface_culling and is_backfacing(dest):
        return
    
    # Get the texture data
    data_array = pygame.surfarray.pixels3d(texture)
    
    # Calculate the area of the triangle in screen space
    area = (dest_x2 - dest_x1) * (dest_y0 - dest_y1) - (dest_x0 - dest_x1) * (dest_y2 - dest_y1)
    if area == 0:
        return
    
    # Loop through the bounding box of the triangle
    min_y = clamp(min(dest_y1, dest_y2, dest_y0), 0, Window.Instance.height)
    min_x = clamp(min(dest_x1, dest_x2, dest_x0), 0, Window.Instance.width)
    max_y = clamp(max(dest_y1, dest_y2, dest_y0), 0, Window.Instance.height)
    max_x = clamp(max(dest_x1, dest_x2, dest_x0), 0, Window.Instance.width)
    
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            # Calculate the barycentric coordinates
            w0 = ((dest_x2 - dest_x1) * (y - dest_y1) - (dest_y2 - dest_y1) * (x - dest_x1)) / area
            w1 = ((dest_x0 - dest_x2) * (y - dest_y2) - (dest_y0 - dest_y2) * (x - dest_x2)) / area
            w2 = 1 - w0 - w1
            
            # Check if the point is inside the triangle
            if 0 <= w0 <= 1 and 0 <= w1 <= 1 and 0 <= w2 <= 1:
                # Calculate the perspective-corrected depth
                z = 1 / (w0 / dest_z0 + w1 / dest_z1 + w2 / dest_z2)
                # Calculate the perspective-corrected texture coordinates
                u = z * (w0 * src_x0 / dest_z0 + w1 * src_x1 / dest_z1 + w2 * src_x2 / dest_z2)
                v = z * (w0 * src_y0 / dest_z0 + w1 * src_y1 / dest_z1 + w2 * src_y2 / dest_z2)

                u = int(u) % tex_w
                v = int(v) % tex_h
                
                # Get the color from the texture and draw it on the screen
                color = data_array[u, v]
                Window.Instance.surface.set_at((x, y), color)


class TriangleDrawer:
    Buffer = []
    def __init__(self, texture, src, dest, depth):
        self.texture = texture
        self.src = src
        self.dest = dest
        self.depth = depth
        self.double_sided = False
    
    @staticmethod
    def SortBuffer():
        TriangleDrawer.Buffer.sort(key=lambda td: td.depth, reverse=True)

    @staticmethod
    def DrawBuffer():
        for tri in TriangleDrawer.Buffer:
            draw_texture_trapezoid(tri.src, tri.dest, tri.texture, not tri.double_sided)

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