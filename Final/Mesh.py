import pygame
from Math import *
from Component import *
from Renderer3D import *
from Window import *
from Camera import *

from numpy import matrix

WHITE = (255, 255, 255)

class Face:
    def __init__(self, indexPoints, uv = None, texture = None):
        self.indexPoints = indexPoints
        self.uv = uv # [[u, v], [u, v], [u, v]]
        self.texture = texture
        self.normal = [0, 0, 0]
        self.depth = 0
        self.length = len(indexPoints)

    def Render(self, camera, new_points):
        #self.RenderWireframe(camera, new_points)
        #return
        if self.texture is None or self.length < 3 or self.length > 4 or self.uv is None:
            return
        self.CalculateDepth(new_points)
        if self.depth < 0:
            return
        self.CalculateNormal(new_points)
        #if self.IsCulled(new_points, camera):
        #    return
        self.RenderTexture(camera, new_points)
        
    def CalculateNormal(self, new_points):
        points = [new_points[i] for i in self.indexPoints]
        v1 = [points[1][j] - points[0][j] for j in range(3)]
        v2 = [points[2][j] - points[0][j] for j in range(3)]
        self.normal = [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]

    def CalculateDepth(self, new_points):
        self.depth = sum([new_points[i][2] for i in self.indexPoints]) / self.length

    def IsCulled(self, new_points, camera):
        view_vector = [new_points[
            self.indexPoints[0]][j] - camera.transform.position[j] for j in range(3)]
        dot_product = sum(self.normal[j] * view_vector[j] for j in range(3))
        return dot_product < 0
    
    def RenderTexture(self, camera, new_points):
        src_coords = self.uv
        dest_coords = [new_points[i][:2] for i in self.indexPoints]
        if self.length == 3:
            TriangleDrawerAppend(src_coords, dest_coords, self.texture, self.depth)
        else:
            QuadDrawerAppend(src_coords, dest_coords, self.texture, self.depth)

    def RenderWireframe(self, camera, new_points):
        for i in range(self.length):
            p0 = new_points[self.indexPoints[i]]
            p1 = new_points[self.indexPoints[(i + 1) % self.length]]
            pygame.draw.line(Window.Instance.surface, WHITE, (p0[0], p0[1]), (p1[0], p1[1]))

class Mesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

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


class MeshRenderer(Component):
    def __init__(self, mesh = None):
        super().__init__()
        self.mesh = mesh

    def OnRender(self):
        if Camera.MainCamera is None or self.mesh is None:
            return
        camera = Camera.MainCamera
        new_points = self.get_transformed_points(camera)
        for face in self.mesh.faces:
            face.Render(camera, new_points)

    def get_transformed_points(self, camera):
        transformed_points = []
        for p in self.mesh.vertices:
            p = [p[i] * self.transform.scale[i] for i in range(3)]
            m = matrix([[p[0]], [p[1]], [p[2]], [1]])
            for method, angle in zip((generate_x, generate_y, generate_z), self.transform.rotation.tolist()):
                m = method(angle) * m[:3, :]
            m[:3, :] += matrix([[self.transform.position.x], [self.transform.position.y], [self.transform.position.z]])
            m[:3, :] -= matrix([[camera.transform.position.x], [camera.transform.position.y], [camera.transform.position.z]])
            for method, angle in zip((generate_x, generate_y, generate_z), camera.transform.rotation.tolist()):
                m = method(angle) * m[:3, :]
            x, y, z = m[:3, 0]
            z = float(z)
            f = 300 / max(1, z)
            x, y = int(x * f + Window.Instance.width / 2), int(-y * f + Window.Instance.height / 2)
            transformed_points.append((x, y, z))
        return transformed_points