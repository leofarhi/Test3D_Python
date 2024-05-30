import pygame
import numpy as np


# Example usage
pygame.init()
screen = pygame.display.set_mode((500, 500))
#square points :
points = [(0, 0), (100, 0), (100, 100), (0, 100)]
points = [(20, 0), (90, 20), (100, 90), (0, 120)]
#[top left, top right, bottom right, bottom left] of new polygon

    
texture = pygame.image.load('texture.jpg').convert_alpha()

def lerp(a, b, t):
    return a + (b - a) * t

def draw_texture_poly(surface, points, texture):
    #la texture est un carre et on veut la mettre sur un polygone quelconque
    data_array = pygame.surfarray.pixels3d(texture)
    #on recupere les dimensions de la texture
    tex_w, tex_h = texture.get_size()
    #on recupere les dimensions du polygone
    H = abs(points[0][1] - points[2][1])
    for i in range(H):
        V = i / H
        #on recupere les coordonnees des extremites du polygone
        w = lerp(points[1][0] - points[0][0], points[2][0] - points[3][0], V)
        x1 = lerp(points[0][0], points[3][0], V)
        x2 = lerp(points[1][0], points[2][0], V)
        y = lerp(points[0][1], points[2][1], V)
        #on recupere les coordonnees des extremites de la premiere ligne de la texture
        u1 = 0
        u2 = tex_w
        for j in range(int(x1), int(x2)):
            #on recupere les coordonnees du pixel
            u = int(lerp(u1, u2, (j - x1) / (x2 - x1))) % tex_w
            v = int(V * tex_h) % tex_h
            #on met la couleur du pixel dans le polygone
            surface.set_at((j, int(y)), data_array[u, v])



done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        points = [(x - 1, y) for x, y in points]
    if keys[pygame.K_RIGHT]:
        points = [(x + 1, y) for x, y in points]
    if keys[pygame.K_UP]:
        points = [(x, y - 1) for x, y in points]
    if keys[pygame.K_DOWN]:
        points = [(x, y + 1) for x, y in points]
    if keys[pygame.K_a]:
        points[0] = (points[0][0] - 1, points[0][1])
        points[1] = (points[1][0] - 1, points[1][1])
    if keys[pygame.K_s]:
        points[0] = (points[0][0] + 1, points[0][1])
        points[1] = (points[1][0] + 1, points[1][1])
    if keys[pygame.K_d]:
        points[0] = (points[0][0], points[0][1] - 1)
    if keys[pygame.K_f]:
        points[0] = (points[0][0], points[0][1] + 1)

    
    screen.fill((0, 0, 0))
    draw_texture_poly(screen, points, texture)
    pygame.display.flip()

pygame.quit()
