import pygame

class Window(object):
    def __init__(self, caption,size_x=800,size_y=600):
        self.size_x = size_x
        self.size_y = size_y
        self.caption = caption
             

    def show(self):
        running = True
        pygame.init()
        self.display = pygame.display.set_mode((self.size_x, self.size_y), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.caption)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
