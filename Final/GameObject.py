from Struct import *
class Transform:
    def __init__(self, position, rotation, scale, gameObject):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.gameObject = gameObject
        self.parent = None


class GameObject:
    def __init__(self, position = None, rotation = None, scale = None):
        if position is None:
            position = Vector3(0, 0, 0)
        if rotation is None:
            rotation = Vector3(0, 0, 0)
        if scale is None:
            scale = Vector3(1, 1, 1)
        self.name = "GameObject"
        self.transform = Transform(position, rotation, scale, self)
        self.activeSelf = True
        self.components = []
        self.scene = None

    @property
    def activeInHierarchy(self):
        return self.activeSelf and (self.parent is None or self.parent.activeInHierarchy)

    def AddComponent(self, component):
        self.components.append(component)
        component.gameObject = self
        return component
    
    def RemoveComponent(self, component):
        self.components.remove(component)
        component.gameObject = None

    def Awake(self):
        for component in self.components:
            component.Awake()

    def Start(self):
        for component in self.components:
            component.Start()

    def Update(self):
        for component in self.components:
            component.Update()

    def FixedUpdate(self):
        for component in self.components:
            component.FixedUpdate()

    def LateUpdate(self):
        for component in self.components:
            component.LateUpdate()

    def OnRender(self):
        for component in self.components:
            component.OnRender()

    def OnGUI(self):
        for component in self.components:
            component.OnGUI()

    def OnEnable(self):
        for component in self.components:
            component.OnEnable()

    def OnDisable(self):
        for component in self.components:
            component.OnDisable()

    def OnDestroy(self):
        for component in self.components:
            component.OnDestroy()

    def GetComponent(self, componentType):
        for component in self.components:
            if isinstance(component, componentType):
                return component
        return None
    
    def GetComponents(self, componentType):
        components = []
        for component in self.components:
            if isinstance(component, componentType):
                components.append(component)
        return components