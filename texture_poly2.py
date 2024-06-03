import pygame
import math

WIDTH = 500
HEIGHT = 500

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

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
    if area == 0:
        return
    
    # Loop through the bounding box of the triangle
    min_y = clamp(min(dest_y1, dest_y2, dest_y0), 0, HEIGHT)
    min_x = clamp(min(dest_x1, dest_x2, dest_x0), 0, WIDTH)
    max_y = clamp(max(dest_y1, dest_y2, dest_y0), 0, HEIGHT)
    max_x = clamp(max(dest_x1, dest_x2, dest_x0), 0, WIDTH)
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            # Calculate the barycentric coordinates
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
                surface.set_at((x, y), color)

def draw_texture_quad(src, dest, texture):
    # Extract source and destination points
    top_left, top_right, bottom_right, bottom_left = src
    top_left_dest, top_right_dest, bottom_right_dest, bottom_left_dest = dest
    
    # Draw the two triangles that form the quad
    draw_texture_tri((top_left, bottom_right, bottom_left), (top_left_dest, bottom_right_dest, bottom_left_dest), texture)
    draw_texture_tri((top_left, top_right, bottom_right), (top_left_dest, top_right_dest, bottom_right_dest), texture)

# Initialize Pygame and create the surface
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texture Triangle")

# Load a texture (example: a 100x100 pixel image)
texture = pygame.image.load('texture2.jpg').convert()

src = [(0, 0), (texture.get_width() - 1, 0), (texture.get_width() - 1, texture.get_height() - 1), (0, texture.get_height() - 1)]
dest = [[100, 100], [300, 100], [300, 300], [100, 300]]


# Main loop to display the result
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #clear the screen
    surface.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dest[2][0] += 50
        dest[3][0] -= 50
        dest[2][1] += 50
        dest[3][1] += 50

    draw_texture_quad(src, dest, texture)

    pygame.display.flip()
    
pygame.quit()
