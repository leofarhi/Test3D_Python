import pygame
from math import cos, sin, pi
from numpy import matrix
from time import sleep
from random import randint


WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 500

pygame.init()
display = pygame.display
surface = display.set_mode((WIDTH, HEIGHT))
display.set_caption("3D")


done = False
points = (
    ( 50,  50,  50),
    (-50,  50,  50),
    ( 50, -50,  50),
    ( 50,  50, -50),
    (-50,  50, -50),
    ( 50, -50, -50),
    (-50, -50, -50),
    (-50, -50,  50),
)

rotation = [0, 0, 0]

def lerp(a, b, t):
    return a + (b - a) * t

MAX_VALUE = 100
cos_lst = []
sin_lst = []
#generate list of cos and sin values
for i in range(MAX_VALUE):
    i = lerp(0, pi, i / MAX_VALUE)
    cos_lst.append(cos(i))
    sin_lst.append(sin(i))

def cos(x):
    x = int(x % pi * MAX_VALUE / pi)
    return cos_lst[x]

def sin(x):
    x = int(x % pi * MAX_VALUE / pi)
    return sin_lst[x]


def generate_x(theta):
    return matrix([
        [1, 0, 0],
        [0, cos(theta), -sin(theta)],
        [0, sin(theta), cos(theta)]
    ])

def generate_y(theta):
    return matrix([
        [cos(theta), 0, -sin(theta)],
        [0, 1, 0],
        [sin(theta), 0, cos(theta)]
    ])

def generate_z(theta):
    return matrix([
        [cos(theta), -sin(theta), 0],
        [sin(theta), cos(theta), 0],
        [0, 0, 1]
    ])

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
            break

    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT))

    render_points = []

    for p in points:

        m = matrix([
        [p[0]],
        [p[1]],
        [p[2]]
        ])

        for method, angle in zip((generate_x, generate_y, generate_z), rotation):
            m = method(angle) * m

        x, y, z = map(lambda x: int(WIDTH/2 - x), (m[0,0], m[1,0], m[2,0]))

        render_points.append((x, y))

    for p1 in range(len(render_points) - 1):
        for p2 in render_points[p1 + 1:]:
            pygame.draw.line(surface, WHITE, render_points[p1], p2)
    #color point in red
    for p in render_points:
        pygame.draw.circle(surface, (255, 0, 0), p, 3)

    rotation[0] += pi / randint(100, 200)
    rotation[1] += pi / randint(100, 200)

    display.flip()
    sleep(1/45)

