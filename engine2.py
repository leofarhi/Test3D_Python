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

MAX_VALUE = 100
cos_lst = []
sin_lst = []

def lerp(a, b, t):
    return a + (b - a) * t

# Generate list of cos and sin values
for i in range(MAX_VALUE):
    angle = lerp(0, pi, i / MAX_VALUE)
    cos_lst.append(cos(angle))
    sin_lst.append(sin(angle))

def lerp(a, b, t):
    return a + (b - a) * t

def cos_approx(x):
    x = int(x % pi * MAX_VALUE / pi)
    return cos_lst[x]

def sin_approx(x):
    x = int(x % pi * MAX_VALUE / pi)
    return sin_lst[x]

def generate_x(theta):
    return matrix([
        [1, 0, 0],
        [0, cos_approx(theta), -sin_approx(theta)],
        [0, sin_approx(theta), cos_approx(theta)]
    ])

def generate_y(theta):
    return matrix([
        [cos_approx(theta), 0, -sin_approx(theta)],
        [0, 1, 0],
        [sin_approx(theta), 0, cos_approx(theta)]
    ])

def generate_z(theta):
    return matrix([
        [cos_approx(theta), -sin_approx(theta), 0],
        [sin_approx(theta), cos_approx(theta), 0],
        [0, 0, 1]
    ])

class Cube:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.points = [
            ( size,  size,  size),
            (-size,  size,  size),
            ( size, -size,  size),
            ( size,  size, -size),
            (-size,  size, -size),
            ( size, -size, -size),
            (-size, -size, -size),
            (-size, -size,  size),
        ]
        self.rotation = [0, 0, 0]

    def rotate(self):
        self.rotation[0] += pi / randint(100, 200)
        self.rotation[1] += pi / randint(100, 200)

    def get_transformed_points(self):
        transformed_points = []
        for p in self.points:
            m = matrix([[p[0]], [p[1]], [p[2]]])
            for method, angle in zip((generate_x, generate_y, generate_z), self.rotation):
                m = method(angle) * m
            x, y, z = map(lambda v: int(WIDTH/2 - v), (m[0,0], m[1,0], m[2,0]))
            transformed_points.append((x + self.center[0], y + self.center[1]))
        return transformed_points

class Camera:
    def __init__(self):
        self.cubes = []

    def add_cube(self, cube):
        self.cubes.append(cube)

    def render(self):
        for cube in self.cubes:
            render_points = cube.get_transformed_points()
            for p1 in range(len(render_points) - 1):
                for p2 in render_points[p1 + 1:]:
                    pygame.draw.line(surface, WHITE, render_points[p1], p2)
            for p in render_points:
                pygame.draw.circle(surface, (255, 0, 0), p, 3)
            cube.rotate()

# Create a camera and add cubes to it
camera = Camera()
camera.add_cube(Cube((0, 0), 50))
camera.add_cube(Cube((100, 100), 30))
camera.add_cube(Cube((-100, -100), 40))

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
            break

    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT))

    camera.render()

    display.flip()
    sleep(1/45)
