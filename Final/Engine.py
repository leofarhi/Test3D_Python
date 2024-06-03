import pygame
from Math import *
from Window import *
from SceneManager import *
from Camera import *
from GameObject import *
from Mesh import *

MainScene = Scene()
MainCamera = MainScene.AddGameObject(GameObject())
MainCamera.AddComponent(Camera())
MainCamera.AddComponent(FreeCam())

MeshObject = MainScene.AddGameObject(GameObject())
meshCompo = MeshObject.AddComponent(MeshRenderer())

size = 100
points = [
    (-size,  size,  size),
    ( size,  size,  size),
    ( size, -size,  size),
    (-size, -size,  size),

    (-size,  size, -size),
    ( size,  size, -size),
    ( size, -size, -size),
    (-size, -size, -size),
]
meshCompo.vertices = points
faces = [
    [1, 0, 3, 2],
    [4, 5, 6, 7],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [0, 4, 7, 3],
    [5, 1, 2, 6]
]
texture = pygame.image.load('texture.jpg').convert()
w, h = texture.get_size()
uv = [(0, 0), (w-1, 0), (w-1, h-1), (0, h-1)]
faces = [Face(f,uv,texture) for f in faces]
meshCompo.mesh = Mesh(points, faces)

MainCamera.transform.position.z = -500
MeshObject.transform.position.z = 100

SceneManager.Manager.LoadScene(MainScene)

while Window.Instance.IsRunning:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            Window.Instance.IsRunning = False
            break
    Window.Instance.Clear()
    SceneManager.Manager.Update()
    #print(MainCamera.transform.position)
    Window.Instance.Update()

Window.Instance.Close()