import pygame
from Math import *
from Struct import *
from Component import *
from Window import *

class Camera(Component):
    MainCamera = None
    def __init__(self):
        super().__init__()
        if Camera.MainCamera is None:
            Camera.MainCamera = self


class FreeCam(Component):
    def __init__(self, speed = 1):
        super().__init__()
        self.speed = speed

    @property
    def position(self):
        return self.transform.position
    
    @property
    def rotation(self):
        return self.transform.rotation

    def rotate(self, axis, angle):
        self.transform.rotation[axis] += angle

    def move(self, axis, distance):
        self.transform.position[axis] += distance

    def Update(self):
        self.inputs(Window.Instance.Keys)

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