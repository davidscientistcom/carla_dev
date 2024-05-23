import pygame
import numpy as np


class MultiScreenCamera(object):

    def __init__(self,screen_width=800,screen_height=600,):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.display = pygame.display.set_mode(
        (800, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Carla Simulation")

        # Definimos los cuadrantes.
        self.quad1 = pygame.Rect(0, 0, screen_width // 2, screen_height // 2)
        self.quad2 = pygame.Rect(screen_width // 2, 0, screen_width // 2, screen_height // 2)
        self.quad3 = pygame.Rect(0, screen_height // 2, screen_width // 2, screen_height // 2)
        self.quad4 = pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 2)
        
        self.quads = {
            1: self.quad1,
            2: self.quad2,
            3: self.quad3,
            4: self.quad4
        }
    def resize_image(self,image, rect):
        return pygame.transform.scale(image, (rect.width, rect.height))

    def draw_image(self,image, quad_region, blend=False):
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        if blend:
            image_surface.set_alpha(100)
        self.display.blit(self.resize_image(image_surface,self.quads.get(quad_region, None)),self.quads.get(quad_region, None))      


    def get_font(self):
        fonts = [x for x in pygame.font.get_fonts()]
        default_font = 'ubuntumono'
        font = default_font if default_font in fonts else fonts[0]
        font = pygame.font.match_font(font)
        return pygame.font.Font(font, 14)





