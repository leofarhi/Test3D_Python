import pygame


#draw_texture_tri(src[3][2],dest[3][2], texture)
#src : source texture coordinates (u, v)
#dest : destination screen coordinates (x, y)
def draw_texture_tri(src, dest, texture):
    # Extract source and destination points
    (src_x0, src_y0), (src_x1, src_y1), (src_x2, src_y2) = src
    (dest_x0, dest_y0), (dest_x1, dest_y1), (dest_x2, dest_y2) = dest
    
    # Get the texture size
    tex_w, tex_h = texture.get_size()
    
    # Get the texture data
    data_array = pygame.surfarray.pixels3d(texture)
    
    # Calculate the area of the triangle
    area = (dest_x1 - dest_x0) * (dest_y2 - dest_y0) - (dest_x2 - dest_x0) * (dest_y1 - dest_y0)
    
    # Loop through the bounding box of the triangle
    for y in range(min(dest_y0, dest_y1, dest_y2), max(dest_y0, dest_y1, dest_y2)):
        for x in range(min(dest_x0, dest_x1, dest_x2), max(dest_x0, dest_x1, dest_x2)):
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

    

# Initialize Pygame and create the surface
pygame.init()
surface = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Texture Triangle")

# Load a texture (example: a 100x100 pixel image)
texture = pygame.image.load('texture.jpg').convert()

# Define source texture coordinates (u, v)
src_coords = [(0, 0), ((texture.get_width() - 1), 0), (0, (texture.get_height() - 1))]

# Define destination screen coordinates (x, y)
#test: dest_coords = [(100, 100), (300, 150), (100, 300)]
# Draw the textured triangle
#draw_texture_tri(src_coords, dest_coords, texture)

#square points :
points1 = [(0, 0), (100, 0), (0, 100)]
points2 = [(100, 0), (100, 100), (0, 100)]
#source texture coordinates (u, v)
w, h = texture.get_size()
src_coords1 = [(0, 0), (w, 0), (0, h)]
src_coords2 = [(w, 0), (w, h), (0, h)]
draw_texture_tri(src_coords1, points1, texture)
draw_texture_tri(src_coords2, points2, texture)

# Main loop to display the result
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    
pygame.quit()
