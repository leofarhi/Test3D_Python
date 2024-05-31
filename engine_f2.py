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

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

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
    mini1 = clamp(mini1, 0, HEIGHT)
    mini2 = clamp(mini2, 0, WIDTH)
    maxi1 = clamp(maxi1, 0, HEIGHT)
    maxi2 = clamp(maxi2, 0, WIDTH)
    ############
    for y in range(mini1, maxi1):
        for x in range(mini2, maxi2):
            # Calculate the barycentric coordinates
            if area == 0 or x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT:
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


def draw_texture_quad(src, dest, texture):
    # Extract source and destination points
    top_left, top_right, bottom_right, bottom_left = src
    top_left_dest, top_right_dest, bottom_right_dest, bottom_left_dest = dest
    
    # Draw the two triangles that form the quad
    draw_texture_tri((top_left, bottom_right, bottom_left), (top_left_dest, bottom_right_dest, bottom_left_dest), texture)
    draw_texture_tri((top_left, top_right, bottom_right), (top_left_dest, top_right_dest, bottom_right_dest), texture)

class Cube:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.points = [
            (-size,  size,  size),
            ( size,  size,  size),
            ( size, -size,  size),
            (-size, -size,  size),

            (-size,  size, -size),
            ( size,  size, -size),
            ( size, -size, -size),
            (-size, -size, -size),
        ]
        self.rotation = [0, 0, 0]
        self.texture = pygame.image.load('texture2.jpg').convert()

    def rotate(self, axis, angle):
        self.rotation[axis] += angle

    def get_transformed_points(self, camera):
        transformed_points = []
        depths_points = []
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
                f = 300 / z
                x, y = int(x * f + WIDTH / 2), int(-y * f + HEIGHT / 2)
                transformed_points.append((x, y))
                depths_points.append(z)
            else:
                transformed_points.append((0, 0))
                depths_points.append(0)
        return transformed_points, depths_points
    
    def render(self, camera):
        render_points, depths_points = self.get_transformed_points(camera)
        self.render_texture(camera, render_points, depths_points)

    def render_texture(self, camera, render_points, dps):
        faces = [
            (render_points[1], render_points[0], render_points[3], render_points[2]),#Back face
            (render_points[4], render_points[5], render_points[6], render_points[7]),#Front face
            (render_points[0], render_points[1], render_points[5], render_points[4]),#Top face
            (render_points[2], render_points[3], render_points[7], render_points[6]),#Bottom face
            (render_points[0], render_points[4], render_points[7], render_points[3]),#Left face
            (render_points[5], render_points[1], render_points[2], render_points[6])#Right face
        ]
        depths = [
            sum(dps[0:4]) / 4,#Back face
            sum(dps[4:8]) / 4,#Front face
            sum([dps[1], dps[0], dps[3], dps[2]]) / 4,#Top face
            sum([dps[2], dps[3], dps[7], dps[6]]) / 4,#Bottom face
            sum([dps[0], dps[4], dps[7], dps[3]]) / 4,#Left face
            sum([dps[5], dps[1], dps[2], dps[6]]) / 4#Right face
        ]
        points = [
            [self.points[1], self.points[0], self.points[3], self.points[2]],#Back face
            [self.points[4], self.points[5], self.points[6], self.points[7]],#Front face
            [self.points[0], self.points[1], self.points[5], self.points[4]],#Top face
            [self.points[2], self.points[3], self.points[7], self.points[6]],#Bottom face
            [self.points[0], self.points[4], self.points[7], self.points[3]],#Left face
            [self.points[5], self.points[1], self.points[2], self.points[6]]#Right face
        ]
        #Cull back faces
        CulledFaces = []
        for i, point in enumerate(points):
            face = faces[i]
            # Calculate vectors
            v1 = [point[1][j] - point[0][j] for j in range(3)]
            v2 = [point[2][j] - point[0][j] for j in range(3)]
            
            # Cross product to get the normal
            normal = [
                v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]
            ]
            
            # Vector from camera to face
            view_vector = [point[0][j] - camera.position[j] for j in range(3)]
            
            # Dot product to determine if the face is visible
            dot_product = sum(normal[j] * view_vector[j] for j in range(3))
            
            if dot_product < 0:
                CulledFaces.append((depths[i], face))

        # Sort faces by depth
        CulledFaces.sort(reverse=True, key=lambda x: x[0])

        #Send the faces to the QuadDrawer
        w, h = self.texture.get_size()
        src_coords = [(0, 0), (w-1, 0), (w-1, h-1), (0, h-1)]
        for depth, face in CulledFaces:
            QuadDrawerAppend(src_coords, face, self.texture, depth)

def QuadDrawerAppend(src, dest, texture, depth):
    top_left, top_right, bottom_right, bottom_left = src
    top_left_dest, top_right_dest, bottom_right_dest, bottom_left_dest = dest

    src = (top_left, bottom_right, bottom_left)
    dest = (top_left_dest, bottom_right_dest, bottom_left_dest)
    TriangleDrawer.Buffer.append(TriangleDrawer(texture, src, dest, depth))
    src = (top_left, top_right, bottom_right)
    dest = (top_left_dest, top_right_dest, bottom_right_dest)
    TriangleDrawer.Buffer.append(TriangleDrawer(texture, src, dest, depth))

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
        TriangleDrawer.ClearBuffer()
        for cube in self.cubes:
            cube.render(self)
        TriangleDrawer.SortBuffer()
        TriangleDrawer.DrawBuffer()
    
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
        if keys[pygame.K_PAGEUP]:
            self.move(1, 10)
        if keys[pygame.K_PAGEDOWN]:
            self.move(1, -10)

    def inputs_local(self, keys):
        if keys[pygame.K_LEFT]:
            self.position[0] += cos(self.rotation[1]) * 10
            self.position[2] += sin(self.rotation[1]) * 10
        if keys[pygame.K_RIGHT]:
            self.position[0] -= cos(self.rotation[1]) * 10
            self.position[2] -= sin(self.rotation[1]) * 10
        if keys[pygame.K_DOWN]:
            self.position[0] -= sin(self.rotation[1]) * 10
            self.position[2] += cos(self.rotation[1]) * 10
        if keys[pygame.K_UP]:
            self.position[0] += sin(self.rotation[1]) * 10
            self.position[2] -= cos(self.rotation[1]) * 10

camera = Camera([0, 0, -500])
camera.add_cube(Cube([0, 0, 100], 50))
camera.add_cube(Cube([0, 0, 200], 50))

while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]:
        camera.cubes[0].rotate(1, pi / 180)
    if keys[pygame.K_p]:
        camera.cubes[0].rotate(1, -pi / 180)
    if keys[pygame.K_l]:
        camera.cubes[0].rotate(0, pi / 180)
    if keys[pygame.K_m]:
        camera.cubes[0].rotate(0, -pi / 180)
    camera.inputs(keys)

    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT))
    camera.render()
    display.flip()
    clock.tick(60)
