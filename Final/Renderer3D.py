import pygame
from Math import *
from Window import *

#draw_texture_tri(src[3][2],dest[3][2], texture)
#src : source texture coordinates (u, v)
#dest : destination screen coordinates (x, y)
def is_backfacing(dest):
    (dest_x0, dest_y0), (dest_x1, dest_y1), (dest_x2, dest_y2) = dest
    return (dest_x1 - dest_x0) * (dest_y2 - dest_y0) - (dest_x2 - dest_x0) * (dest_y1 - dest_y0) < 0

def Recalculate(src, dest):
    (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2) = src
    (dest_x0, dest_y0), (dest_x1, dest_y1), (dest_x2, dest_y2) = dest

    screen_width = Window.Instance.width
    screen_height = Window.Instance.height

    def clip(v0, v1, v2, t0, t1, t2, clip_val, is_x_clip=True):
        if is_x_clip:
            if v0 < 0 and v1 < 0 and v2 < 0:
                return []
            if v0 > clip_val and v1 > clip_val and v2 > clip_val:
                return []

            if v0 < 0 or v1 < 0 or v2 < 0:
                # Clipping logic for when points are off the left or right of the screen
                pass
            if v0 > clip_val or v1 > clip_val or v2 > clip_val:
                # Clipping logic for when points are off the left or right of the screen
                pass
        else:
            if v0 < 0 and v1 < 0 and v2 < 0:
                return []
            if v0 > clip_val and v1 > clip_val and v2 > clip_val:
                return []

            if v0 < 0 or v1 < 0 or v2 < 0:
                # Clipping logic for when points are off the top or bottom of the screen
                pass
            if v0 > clip_val or v1 > clip_val or v2 > clip_val:
                # Clipping logic for when points are off the top or bottom of the screen
                pass

        return [(v0, t0), (v1, t1), (v2, t2)]

    # Clipping for X coordinates
    result = clip(dest_x0, dest_x1, dest_x2, (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2), screen_width, True)
    if not result:
        return None, None
    (dest_x0, src_x0), (dest_x1, src_x1), (dest_x2, src_x2) = result

    # Clipping for Y coordinates
    result = clip(dest_y0, dest_y1, dest_y2, (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2), screen_height, False)
    if not result:
        return None, None
    (dest_y0, src_y0), (dest_y1, src_y1), (dest_y2, src_y2) = result

    return [(src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2)], [(dest_x0, dest_y0), (dest_x1, dest_y1), (dest_x2, dest_y2)]



def draw_texture_tri(src, dest, texture, backface_culling = True):
    # Extract source and destination points
    (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2) = src
    (dest_x0, dest_y0), (dest_x1, dest_y1), (dest_x2, dest_y2),  = dest

    if backface_culling and is_backfacing(dest):
        return
    
    #src, dest = Recalculate(src, dest)
    if src is None or dest is None:
        return
    # Get the texture size
    tex_w, tex_h = texture.get_size()
    
    # Get the texture data
    data_array = pygame.surfarray.pixels3d(texture)
    
    # Calculate the area of the triangle
    area = (dest_x2 - dest_x1) * (dest_y0 - dest_y1) - (dest_x0 - dest_x1) * (dest_y2 - dest_y1)
    if area == 0:
        return
    # Bounding box of the triangle
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
                # Calculate the texture coordinates
                u = w0 * src_x0 + w1 * src_x1 + w2 * src_x2
                v = w0 * src_y0 + w1 * src_y1 + w2 * src_y2
                u = int(u) % tex_w
                v = int(v) % tex_h
                
                # Get the color from the texture and draw it on the screen
                color = data_array[u, v]
                Window.Instance.surface.set_at((x, y), color)

#def draw_texture_tri(src, dest, texture, backface_culling = True):
#    draw_uvmap_tri(src, dest, backface_culling)

def draw_uvmap_tri(src, dest, backface_culling = True):
    # Extract source and destination points
    (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2) = src
    (dest_x0, dest_y0), (dest_x1, dest_y1), (dest_x2, dest_y2) = dest

    if backface_culling and is_backfacing(dest):
        return
    
    # Get the texture size
    tex_w, tex_h = Window.Instance.width, Window.Instance.height
    
    # Calculate the area of the triangle
    area = (dest_x2 - dest_x1) * (dest_y0 - dest_y1) - (dest_x0 - dest_x1) * (dest_y2 - dest_y1)
    if area == 0:
        return
    
    # Bounding box of the triangle
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
                # Calculate the texture coordinates
                u = w0 * src_x0 + w1 * src_x1 + w2 * src_x2
                v = w0 * src_y0 + w1 * src_y1 + w2 * src_y2
                u = int(u) % tex_w
                v = int(v) % tex_h

                color = (u, v, 0)
                Window.Instance.surface.set_at((x, y), color)

"""
#other implementation
def edge_function(x0, y0, x1, y1, x, y):
    return (y - y0) * (x1 - x0) - (x - x0) * (y1 - y0)

def draw_texture_tri(src, dest, texture, backface_culling=True):
    # Extract source and destination points
    (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2) = src
    (dest_x0, dest_y0), (dest_x1, dest_y1), (dest_x2, dest_y2) = dest

    if backface_culling and is_backfacing(dest):
        return
    
    # Check if source or destination is None
    if src is None or dest is None:
        return
    
    # Get the texture size and data
    tex_w, tex_h = texture.get_size()
    data_array = pygame.surfarray.pixels3d(texture)
    
    # Bounding box of the triangle
    min_y = clamp(min(dest_y1, dest_y2, dest_y0), 0, Window.Instance.height)
    min_x = clamp(min(dest_x1, dest_x2, dest_x0), 0, Window.Instance.width)
    max_y = clamp(max(dest_y1, dest_y2, dest_y0), 0, Window.Instance.height)
    max_x = clamp(max(dest_x1, dest_x2, dest_x0), 0, Window.Instance.width)

    # Precompute edge functions for the triangle
    edge0 = edge_function(dest_x1, dest_y1, dest_x2, dest_y2, dest_x0, dest_y0)
    edge1 = edge_function(dest_x2, dest_y2, dest_x0, dest_y0, dest_x1, dest_y1)
    edge2 = edge_function(dest_x0, dest_y0, dest_x1, dest_y1, dest_x2, dest_y2)
    
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            # Calculate the edge functions for the point
            w0 = edge_function(dest_x1, dest_y1, dest_x2, dest_y2, x, y)
            w1 = edge_function(dest_x2, dest_y2, dest_x0, dest_y0, x, y)
            w2 = edge_function(dest_x0, dest_y0, dest_x1, dest_y1, x, y)
            
            # Check if the point is inside the triangle
            if w0 >= 0 and w1 >= 0 and w2 >= 0:
                # Normalize weights
                total_w = w0 + w1 + w2
                w0 /= total_w
                w1 /= total_w
                w2 /= total_w
                
                # Calculate the texture coordinates
                u = int(w0 * src_x0 + w1 * src_x1 + w2 * src_x2) % tex_w
                v = int(w0 * src_y0 + w1 * src_y1 + w2 * src_y2) % tex_h
                
                # Get the color from the texture and draw it on the screen
                color = data_array[u, v]
                Window.Instance.surface.set_at((x, y), color)
"""




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
        self.double_sided = False
    
    @staticmethod
    def SortBuffer():
        TriangleDrawer.Buffer.sort(key=lambda td: td.depth, reverse=True)

    @staticmethod
    def DrawBuffer():
        for tri in TriangleDrawer.Buffer:
            draw_texture_tri(tri.src, tri.dest, tri.texture, not tri.double_sided)

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