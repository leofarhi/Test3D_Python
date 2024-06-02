class Component:
    def __init__(self):
        self.gameObject = None
        self.enabled = True

    @property
    def transform(self):
        return self.gameObject.transform
    
    @property
    def name(self):
        return self.__class__.__name__

    def GetComponent(self, componentType):
        for component in self.gameObject.components:
            if isinstance(component, componentType):
                return component
        return None
    
    def GetComponents(self, componentType):
        components = []
        for component in self.gameObject.components:
            if isinstance(component, componentType):
                components.append(component)
        return components
    
    def Awake(self):
        pass

    def Start(self):
        pass

    def Update(self):
        pass

    def FixedUpdate(self):
        pass

    def LateUpdate(self):
        pass

    def OnRender(self):
        pass

    def OnGUI(self):
        pass

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass

    def OnDestroy(self):
        pass