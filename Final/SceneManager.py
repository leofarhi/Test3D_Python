from Renderer3D import *

class SceneManager:
    Manager = None
    def __init__(self):
        self.scenes = []
        if SceneManager.Manager is None:
            SceneManager.Manager = self

    def LoadScene(self, scene):
        self.scenes.append(scene)
        scene.Awake()
        scene.Start()

    def render(self):
        TriangleDrawer.SortBuffer()
        TriangleDrawer.DrawBuffer()
        TriangleDrawer.ClearBuffer()

    def UnloadScene(self, scene):
        scene.OnDestroy()
        self.scenes.remove(scene)

    def Update(self):
        for scene in self.scenes:
            scene.FixedUpdate()
        for scene in self.scenes:
            scene.Update()
        for scene in self.scenes:
            scene.LateUpdate()
        for scene in self.scenes:
            scene.OnRender()
        self.render()

class Scene:
    def __init__(self):
        self.gameObjects = []

    def Awake(self):
        for gameObject in self.gameObjects:
            gameObject.Awake()

    def Start(self):
        for gameObject in self.gameObjects:
            gameObject.Start()

    def Update(self):
        for gameObject in self.gameObjects:
            gameObject.Update()

    def FixedUpdate(self):
        for gameObject in self.gameObjects:
            gameObject.FixedUpdate()

    def LateUpdate(self):
        for gameObject in self.gameObjects:
            gameObject.LateUpdate()

    def OnRender(self):
        for gameObject in self.gameObjects:
            gameObject.OnRender()

    def OnGUI(self):
        for gameObject in self.gameObjects:
            gameObject.OnGUI()

    def OnEnable(self):
        for gameObject in self.gameObjects:
            gameObject.OnEnable()

    def OnDisable(self):
        for gameObject in self.gameObjects:
            gameObject.OnDisable()

    def OnDestroy(self):
        for gameObject in self.gameObjects:
            gameObject.OnDestroy()

    def AddGameObject(self, gameObject):
        self.gameObjects.append(gameObject)
        gameObject.scene = self
        return gameObject

    def RemoveGameObject(self, gameObject):
        self.gameObjects.remove(gameObject)

    def FindGameObject(self, name):
        for gameObject in self.gameObjects:
            if gameObject.name == name:
                return gameObject
        return None
    
SceneManager()