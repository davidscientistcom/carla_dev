import pygame
import numpy as np
import carla

class Camera(object):
    def __init__(self,world,vehicle,quad,x,y,z,pitch,yaw,type='sensor.camera.rgb'):
        self.quad = quad
        self.world = world
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.type = type
        blueprint_library = world.get_blueprint_library()        
        self.camera = self.world.spawn_actor(
            blueprint_library.find('sensor.camera.rgb'),
            carla.Transform(carla.Location(x=self.x, z=self.z), carla.Rotation(pitch=self.pitch,yaw=self.yaw)),
            attach_to=vehicle)

 
class MultiScreenCamera(object):

    def __init__(self,world,vehicle,screen_width=800,screen_height=600):
        self.data = []
        self.cameras = []
        self.world = world
        self.vehicle = vehicle
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
        self._addDefaultCameras()
  

    def _addDefaultCameras(self):        
        self.cameras.append(Camera(self.world,self.vehicle,1,x=3,y=0,z=1,pitch=-15,yaw=0)) #Front
        self.cameras.append(Camera(self.world,self.vehicle,2,x=-3,y=0,z=1,pitch=-15,yaw=180)) #Back
        self.cameras.append(Camera(self.world,self.vehicle,3,x=3,y=0,z=1,pitch=-15,yaw=45)) #Right
        self.cameras.append(Camera(self.world,self.vehicle,4,x=3,y=0,z=1,pitch=-15,yaw=-45)) #Left
 

    def resize_image(self,image, rect):
        return pygame.transform.scale(image, (rect.width, rect.height))
    
    def draw(self):
        for i in range (1,len(self.cameras)+1):
            self.draw_image(self.data[i],i)

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
    
    def destroy(self):
        print('destroying cameras.')
        for c in self.cameras:
            c.destroy();


    




