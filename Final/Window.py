import pygame

class Window:
    Instance = None
    def __init__(self, width, height, name):
        pygame.init()
        self.IsRunning = True
        self.name = name
        self.width = width
        self.height = height
        self.display = pygame.display
        self.surface = self.display.set_mode((width, height))
        self.display.set_caption(name)
        Window.Instance = self
        self.Keys = [False] * 512
        
    def Clear(self):
        self.surface.fill((0, 0, 0))
        self.Keys = pygame.key.get_pressed()

    def Update(self):
        self.display.flip()

    def Close(self):
        pygame.quit()

Window(500, 500, "3D")