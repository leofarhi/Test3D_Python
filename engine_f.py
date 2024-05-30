import pygame
from math import cos, sin, pi
from numpy import matrix

WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 500

pygame.init()
display = pygame.display
surface = display.set_mode((WIDTH, HEIGHT))
display.set_caption("3D")

done = False
clock = pygame.time.Clock()

MAX_VALUE = 360
cos_lst = []
sin_lst = []

def lerp(a, b, t):
    return a + (b - a) * t

# Generate list of cos and sin values
for i in range(MAX_VALUE):
    angle = lerp(-pi, pi, i / MAX_VALUE)
    cos_lst.append(cos(angle))
    sin_lst.append(sin(angle))

def cos(x):
    x = int(x % pi * MAX_VALUE / pi)
    return cos_lst[x%MAX_VALUE]

def sin(x):
    x = int(x % pi * MAX_VALUE / pi)
    return sin_lst[x%MAX_VALUE]

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
                surface.set_at((x, y), color)

class Cube:
    def __init__(self, position, size):
        self.position = position
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
        self.texture = pygame.image.load('texture.jpg').convert()

    def rotate(self, axis, angle):
        self.rotation[axis] += angle

    def get_transformed_points(self, camera):
        transformed_points = []
        for p in self.points:
            m = matrix([[p[0]], [p[1]], [p[2]], [1]])
            for method, angle in zip((generate_x, generate_y, generate_z), self.rotation):
                m = method(angle) * m[:3, :]
            m[:3, :] += matrix([[self.position[0]], [self.position[1]], [self.position[2]]])
            m[:3, :] -= matrix([[camera.position[0]], [camera.position[1]], [camera.position[2]]])
            for method, angle in zip((generate_x, generate_y, generate_z), camera.rotation):
                m = method(angle) * m[:3, :]
            x, y, z = m[:3, 0]
            if z > 0:  # Perspective projection
                f = 200 / z
                x, y = int(x * f + WIDTH / 2), int(-y * f + HEIGHT / 2)
                transformed_points.append((x, y))
        return transformed_points
    
    def render(self, camera):
        render_points = self.get_transformed_points(camera)
        for p1 in range(len(render_points) - 1):
            for p2 in render_points[p1 + 1:]:
                pygame.draw.line(surface, WHITE, render_points[p1], p2)
        for p in render_points:
            pygame.draw.circle(surface, (255, 0, 0), p, 3)
        self.render_texture(camera, render_points)

    def render_texture(self, camera, render_points):
        w, h = self.texture.get_size()
        src_coords = [(0, 0), (w, 0), (0, h)]
        #dest_coords = render_points[:3]
        #draw_texture_tri(src_coords, dest_coords, self.texture)
        dest_face1_1 = [render_points[0], render_points[1], render_points[2]]
        dest_face1_2 = [render_points[1], render_points[2], render_points[7]]
        dest_face2_1 = [render_points[0], render_points[2], render_points[3]]
        dest_face2_2 = [render_points[2], render_points[3], render_points[5]]
        dest_face3_1 = [render_points[0], render_points[1], render_points[3]]
        dest_face3_2 = [render_points[1], render_points[3], render_points[4]]
        dest_face4_1 = [render_points[5], render_points[6], render_points[7]]
        dest_face4_2 = [render_points[2], render_points[5], render_points[7]]
        dest_face5_1 = [render_points[4], render_points[1], render_points[7]]
        dest_face5_2 = [render_points[7], render_points[4], render_points[6]]
        dest_face6_1 = [render_points[4], render_points[5], render_points[6]]
        dest_face6_2 = [render_points[4], render_points[5], render_points[3]]
        draw_texture_tri(src_coords, dest_face1_1, self.texture)
        draw_texture_tri(src_coords, dest_face1_2, self.texture)
        draw_texture_tri(src_coords, dest_face2_1, self.texture)
        draw_texture_tri(src_coords, dest_face2_2, self.texture)
        draw_texture_tri(src_coords, dest_face3_1, self.texture)
        draw_texture_tri(src_coords, dest_face3_2, self.texture)
        draw_texture_tri(src_coords, dest_face4_1, self.texture)
        draw_texture_tri(src_coords, dest_face4_2, self.texture)
        draw_texture_tri(src_coords, dest_face5_1, self.texture)
        draw_texture_tri(src_coords, dest_face5_2, self.texture)
        draw_texture_tri(src_coords, dest_face6_1, self.texture)
        draw_texture_tri(src_coords, dest_face6_2, self.texture)

class Camera:
    def __init__(self, position):
        self.position = position
        self.rotation = [0, 0, 0]
        self.cubes = []

    def add_cube(self, cube):
        self.cubes.append(cube)

    def rotate(self, axis, angle):
        self.rotation[axis] += angle

    def move(self, axis, distance):
        self.position[axis] += distance

    def render(self):
        for cube in self.cubes:
            cube.render(self)
    def inputs(self, keys):
        if keys[pygame.K_a]:
            self.rotate(1, pi / 180)
        if keys[pygame.K_d]:
            self.rotate(1, -pi / 180)
        if keys[pygame.K_w]:
            self.rotate(0, pi / 180)
        if keys[pygame.K_s]:
            self.rotate(0, -pi / 180)
        if keys[pygame.K_q]:
            self.rotate(2, pi / 180)
        if keys[pygame.K_e]:
            self.rotate(2, -pi / 180)
        self.inputs_local(keys)
        #self.inputs_global(keys)
        if keys[pygame.K_PAGEUP]:
            self.move(1, 10)
        if keys[pygame.K_PAGEDOWN]:
            self.move(1, -10)


    def inputs_local(self, keys):
        #change movement is adapted with rotation
        if keys[pygame.K_LEFT]:
            #move forward in the direction of the camera
            self.position[0] += cos(self.rotation[1]) * 10
            self.position[2] += sin(self.rotation[1]) * 10
        if keys[pygame.K_RIGHT]:
            #move backward in the opposite direction of the camera
            self.position[0] -= cos(self.rotation[1]) * 10
            self.position[2] -= sin(self.rotation[1]) * 10
        if keys[pygame.K_DOWN]:
            #move left in the direction of the camera
            self.position[0] -= sin(self.rotation[1]) * 10
            self.position[2] += cos(self.rotation[1]) * 10
        if keys[pygame.K_UP]:
            #move right in the direction of the camera
            self.position[0] += sin(self.rotation[1]) * 10
            self.position[2] -= cos(self.rotation[1]) * 10

    def inputs_global(self, keys):
        if keys[pygame.K_UP]:
            self.move(2, 10)
        if keys[pygame.K_DOWN]:
            self.move(2, -10)
        if keys[pygame.K_LEFT]:
            self.move(0, -10)
        if keys[pygame.K_RIGHT]:
            self.move(0, 10)

# Create a camera and add cubes to it
camera = Camera([0, 0, -500])
camera.add_cube(Cube([0, 0, 100], 50))
#camera.add_cube(Cube([100, 100, 200], 30))
#camera.add_cube(Cube([-100, -100, 300], 40))
#camera.add_cube(Cube([-100, -180, 300], 40))
#for i in range(1, 10):
#    camera.add_cube(Cube([i*100, 0, 300], 40))

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
            break

    keys = pygame.key.get_pressed()
    
    camera.inputs(keys)

    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT))

    camera.render()

    display.flip()
    clock.tick(60)
