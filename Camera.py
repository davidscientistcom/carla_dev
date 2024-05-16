import carla
import numpy as np
import cv2

class Camera(object):

    def __init__(self, world, vehicle, camera_type, pos_x, pos_z, callback, dim_x='640', dim_y='360'):
        self.world = world
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.camera_type = camera_type
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.callback = callback

        
        camera_bp = self.world.get_blueprint_library().find(self.camera_type)
        camera_bp.set_attribute('image_size_x', self.dim_x)
        camera_bp.set_attribute('image_size_y', self.dim_y)

        
        camera_init_trans = carla.Transform(carla.Location(z=self.pos_z, x=self.pos_x))
        
       
        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)
        
        
        image_w = int(self.dim_x)
        image_h = int(self.dim_y)
        self.camera_data = {'image': np.zeros((image_h, image_w, 4))}

        # Comienza a escuchar la cámara usando el callback proporcionado
        self.camera.listen(lambda image: self.callback(image, self.camera_data))

    def render(self,window_name):
        static_image = cv2.imread('image1.jpg')

        while True:
            #cv2.imshow(window_name, self.camera_data['image'])
            cv2.imshow(window_name, static_image)
            # Rompe el bucle si el usuario presiona 'q'
            if cv2.waitKey(1) == ord('q'):
                break
        
        # Limpieza y cierre de recursos
        cv2.destroyAllWindows()
        self.camera.stop()  # Detiene la cámara

